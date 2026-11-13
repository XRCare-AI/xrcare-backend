""" Chatbot model: the data and logic behind the site's chat bubble (same role as model/contact.py)

The chatbot keeps no database table. Each request sends the whole conversation, so the server remembers nothing
between messages; this keeps visitors' chats private and the model simple.

Data here:   SYSTEM_PROMPT (what the bot knows and how it behaves), WIDGET (the bubble's wording),
             PRIVATE_INFO_PATTERNS (personal details that must never reach an AI service),
             PROVIDERS (which AI services to try, in order), and the message limits.
Logic here:  get_reply(history) checks the conversation, then tries each provider in turn.
API keys come from .env (GEMINI_API_KEY, GROQ_API_KEY) and never leave the backend.
"""
import os
import re

import requests


# What the bot is told before every conversation. It only gets the facts below, and is told to stick to them,
# so it does not invent capabilities, prices or medical guidance that XRCare has not approved.
SYSTEM_PROMPT = """You are the assistant on the XRCare AI website. Use only the facts below.

Facts:
- XRCare is a DBA of Plerion AI, Inc. It is building the XR-AI Care Co-Pilot, an extended reality (XR) + AI
  platform for clinical teams, pharmacies and care team training.
- The Co-Pilot is designed to combine vision, speech, sensor and EMR data to help care teams with documentation,
  workflows and safety, with a privacy-first design.
- Site pages: Home (/), About Us (/about-us/), Explore (/explore/: Clinical Teams, Care Team Training, Pharmacy
  and Articles), Contact (/contact/), Log in (/login/) and Get Started (/signup/).
- Contact: info@XRCare.ai or +1-858-324-4114.

Rules:
- Answer in 1 to 3 short sentences of plain text, with no markdown, lists or headings.
- Only answer general questions about XRCare and this website. Politely decline anything else.
- Never give medical advice, diagnoses or treatment information; say a clinician should be asked.
- Do not state or guess prices, availability, release dates, customers, partners, certifications, regulatory
  status, results or any capability not in the facts above. Say you don't have that information and point to
  the Contact page.
- Never ask for personal, health or patient information. If someone shares it, do not repeat it, and remind
  them not to share it here."""

# The bubble's wording. The frontend gets it from GET /api/chat, so it only displays it.
WIDGET = {
    'title': 'XRCare Assistant',
    'greeting': "Hi! I can answer general questions about XRCare and this website.",
    'notice': "General information only, not medical advice. Please don't share personal or patient information.",
    'suggestions': [
        'What is the XR-AI Care Co-Pilot?',
        'Who is XRCare for?',
        'How do I contact the team?',
    ],
    'placeholder': 'Type your question...',
    'send_label': 'Send',
    'open_label': 'Chat with XRCare',
    'close_label': 'Close chat',
    'thinking': 'Thinking...',
}

# Personal details that are blocked before a message is sent to any AI service. Each entry is
# (what to call it, pattern). This only catches details with a recognizable shape; it cannot spot a name or a
# described condition, which is why the notice above also asks visitors not to share them.
PRIVATE_INFO_PATTERNS = [
    ('an email address', re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+')),
    ('a phone number', re.compile(r'(\+?\d[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b')),
    ('a Social Security number', re.compile(r'\b\d{3}-\d{2}-\d{4}\b')),
    ('a date', re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b')),
    ('an ID number', re.compile(r'\b\d{7,}\b')),
    ('a medical record or insurance detail',
     re.compile(r'\b(mrn|medical record|date of birth|dob|patient id|insurance (id|number)|member id)\b', re.I)),
]

# Limits so one visitor cannot run up the API bill or send a huge request (the per-minute limit is in model/rate_limit.py)
MAX_MESSAGES = 20         # only the most recent messages are sent to the AI
MAX_MESSAGE_CHARS = 1000  # per message
TIMEOUT_SECONDS = 20      # give up on a provider that hangs, so the next one can be tried

# Which AI services to try, in order: Gemini first, Groq as the backup if Gemini fails or has no key.
# Model names can be changed in .env without touching code, because providers rename models often.
PROVIDERS = [
    {'name': 'gemini', 'key_env': 'GEMINI_API_KEY', 'model_env': 'GEMINI_MODEL', 'default_model': 'gemini-flash-latest'},
    {'name': 'groq', 'key_env': 'GROQ_API_KEY', 'model_env': 'GROQ_MODEL', 'default_model': 'llama-3.3-70b-versatile'},
]


class ChatError(Exception):
    """ Raised with a message that is safe to show the visitor, and the HTTP status the API should send:
    400 = the visitor's message was bad, 503 = no AI service could answer """
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def find_private_info(text):
    """ Return what kind of personal detail text contains (e.g. 'a phone number'), or None if it has none """
    for label, pattern in PRIVATE_INFO_PATTERNS:
        if pattern.search(text):
            return label
    return None


def clean_history(history):
    """ Check the conversation from the browser and return it as [{'role': 'user'|'assistant', 'content': str}].

    The browser can send anything, so each message is checked before any of it reaches an AI service.
    Raises ChatError if the conversation cannot be used.
    """
    if not isinstance(history, list) or not history:
        raise ChatError("Please type a question.")

    cleaned = []
    for message in history[-MAX_MESSAGES:]:
        if not isinstance(message, dict):
            raise ChatError("That message could not be read.")
        role = message.get('role')
        content = str(message.get('content') or '').strip()
        if role not in ('user', 'assistant') or not content:
            raise ChatError("That message could not be read.")
        if len(content) > MAX_MESSAGE_CHARS:
            raise ChatError(f"Messages can be up to {MAX_MESSAGE_CHARS} characters.")
        # Only the visitor's messages are checked: the bot's own answers include XRCare's public email and phone
        found = find_private_info(content) if role == 'user' else None
        if found:
            raise ChatError(f"For privacy, please don't share {found} or other personal details. "
                            "Your message was not sent.")
        cleaned.append({'role': role, 'content': content})

    # Cutting to the last MAX_MESSAGES can leave an assistant message first; both services expect the user to start
    while cleaned and cleaned[0]['role'] != 'user':
        cleaned.pop(0)
    # The newest message must be the visitor's question, not the bot's own answer
    if not cleaned or cleaned[-1]['role'] != 'user':
        raise ChatError("Please type a question.")
    return cleaned


def ask_gemini(history, api_key, model):
    """ Send the conversation to Google Gemini and return its answer as text """
    # Gemini calls the bot's turns "model" instead of "assistant", and wraps text in "parts"
    contents = [
        {'role': 'model' if m['role'] == 'assistant' else 'user', 'parts': [{'text': m['content']}]}
        for m in history
    ]
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        headers={'x-goog-api-key': api_key},  # in a header, not the URL, so the key never shows up in logs
        json={'systemInstruction': {'parts': [{'text': SYSTEM_PROMPT}]}, 'contents': contents},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    parts = response.json()['candidates'][0]['content']['parts']
    return ''.join(part.get('text', '') for part in parts)


def ask_groq(history, api_key, model):
    """ Send the conversation to Groq and return its answer as text """
    # Groq uses the OpenAI message format: the system prompt is just the first message
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + history
    response = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}'},
        json={'model': model, 'messages': messages, 'max_tokens': 300},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']


# Matches each provider's name in PROVIDERS to the procedure that talks to it
ASK = {'gemini': ask_gemini, 'groq': ask_groq}


def get_reply(history):
    """ Answer the visitor's latest message.

    Parameter: history, the conversation so far: a list of {'role', 'content'} messages ending with the visitor's.
    Returns {'reply': text, 'provider': name of the service that answered}.
    Raises ChatError if the conversation is not allowed or no provider could answer.
    """
    # 1. Check the conversation first, so nothing bad or private is ever sent to an AI service
    history = clean_history(history)

    # 2. Try each provider in order and stop at the first good answer, so the chat keeps working if one is down
    for provider in PROVIDERS:
        api_key = os.environ.get(provider['key_env'])
        if not api_key:
            continue  # no key in .env for this provider: skip it
        model = os.environ.get(provider['model_env']) or provider['default_model']
        try:
            reply = ASK[provider['name']](history, api_key, model).strip()
        except (requests.RequestException, KeyError, IndexError, ValueError) as error:
            # Log the real error for us (never the key), then fall through to the next provider
            print(f"Chat: {provider['name']} failed: {error}")
            continue
        if reply:
            return {'reply': reply, 'provider': provider['name']}

    # 3. Every provider was skipped or failed
    raise ChatError("The assistant isn't available right now. Please try again later or use the Contact page.", 503)


def is_available():
    """ True if at least one provider has a key, so the frontend only shows the bubble when it can answer """
    return any(os.environ.get(provider['key_env']) for provider in PROVIDERS)
