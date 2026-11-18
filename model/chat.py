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


# What the bot is told before every conversation. Every fact below comes from a public source checked in
# November 2026; anything unclear or without a solid source was left out on purpose, so the bot cannot repeat it.
# Sources: xrcare.ai (home), xrcare.ai/about-us, xrcare.ai/contact, evonexus.org ("2025: A Year of Records").
SYSTEM_PROMPT = """You are the assistant on the XRCare AI website. Use only the facts below. They are how XRCare
describes itself, so present product facts as what XRCare says or plans (for example "XRCare describes it as..."),
not as proven results.

Facts about the company:
- XRCare is a DBA (doing-business-as name) of Plerion AI, Inc.
- Founder and CEO: Amin Barhoush. Co-founder and Chief Product Officer: Quyen Ly. CTO: Dr. Haider Ali.
- Plerion AI (XRCare) is in the San Diego cohort of EvoNexus, a nonprofit technology startup incubator in San Diego.
- XRCare's stated mission is to build a trusted XR-AI platform, starting in healthcare and later expanding to
  other fields such as education, industrial work and public safety.
- Contact: email info@XRCare.ai, or the Contact page (/contact/).

Facts about the product:
- XRCare's product is the XR-AI Point-of-Care Co-Pilot (this website calls it the XR-AI Care Co-Pilot), for
  clinical teams, pharmacies and care team training. XRCare's website also describes it as a Spatial AI Nurse
  Co-Pilot.
- The nurse wears lightweight smart glasses. From the nurse's point of view, the co-pilot sees the nurse's hands,
  devices and settings, listens as the nurse describes each step, compares what is happening with the order and
  protocol, and quietly guides the nurse when something does not match, so an error can be caught before it
  reaches the patient.
- XRCare's principle: "The AI suggests. The nurse decides. Always." The nurse stays in control.
- When needed, it can bring an experienced colleague into the nurse's view live through the glasses.
- XRCare says it runs on the device, which keeps it fast and private and keeps patient video in the room, with
  clear consent.
- XRCare plans to start with training (guiding new nurses through real devices and procedures) and later expand
  to the bedside and home health.
- XRCare's website does not say who makes the smart glasses, which devices are supported, prices, release dates,
  customers, partners, regulatory approvals or results.

Site pages: Home (/), About Us (/about-us/), Explore (/explore/: Clinical Teams, Care Team Training, Pharmacy and
Articles), Contact (/contact/), Log in (/login/) and Get Started (/signup/).

Rules:
- Be warm, friendly and professional. Answer in 1 to 3 short sentences of plain text, with no markdown, lists
  or headings.
- Help with general questions about XRCare, who it is for, and finding things on this website.
- You may briefly explain general terms used in the facts above (like XR, AI, spatial AI or EMR) in plain language.
- If a question is related to XRCare but the facts above don't fully answer it, first share whatever the facts
  do say that is relevant, then say you don't have details on that specific point and suggest the Contact page.
  Never invent or guess details that are not in the facts.
- Never give medical advice, diagnoses or treatment information; kindly say a clinician should be asked.
- For questions unrelated to XRCare, briefly and kindly say you can only help with questions about XRCare.
- If someone shares something personal or emotional, respond briefly with kindness, do not ask for details,
  and gently say this chat is only for questions about XRCare.
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
TIMEOUT_SECONDS = 45      # give up on a provider that hangs, so the next one can be tried (OCS's Gemini API allows 90)

# Which AI services to try, in order: Gemini first, Groq as the backup if Gemini fails or has no key.
# Model names can be changed in .env without touching code, because providers rename and retire models often.
# Defaults tested Nov 2026: Flash-Lite answers in 1-3 s (gemini-flash-latest timed out); Groq retired llama-3.3.
PROVIDERS = [
    {'name': 'gemini', 'key_env': 'GEMINI_API_KEY', 'model_env': 'GEMINI_MODEL', 'default_model': 'gemini-3.5-flash-lite'},
    {'name': 'groq', 'key_env': 'GROQ_API_KEY', 'model_env': 'GROQ_MODEL', 'default_model': 'openai/gpt-oss-20b'},
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


def ask_gemini(history, api_key, model, system=SYSTEM_PROMPT, json_only=False):
    """ Send the conversation to Google Gemini and return its answer as text (json_only: ask for JSON) """
    # Gemini calls the bot's turns "model" instead of "assistant", and wraps text in "parts"
    contents = [
        {'role': 'model' if m['role'] == 'assistant' else 'user', 'parts': [{'text': m['content']}]}
        for m in history
    ]
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        headers={'x-goog-api-key': api_key},  # in a header, not the URL, so the key never shows up in logs
        json={'systemInstruction': {'parts': [{'text': system}]}, 'contents': contents,
              **({'generationConfig': {'responseMimeType': 'application/json'}} if json_only else {})},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    parts = response.json()['candidates'][0]['content']['parts']
    return ''.join(part.get('text', '') for part in parts)


def ask_groq(history, api_key, model, system=SYSTEM_PROMPT, json_only=False):
    """ Send the conversation to Groq and return its answer as text (json_only: ask for JSON) """
    # Groq uses the OpenAI message format: the system prompt is just the first message
    messages = [{'role': 'system', 'content': system}] + history
    response = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {api_key}'},
        json={'model': model, 'messages': messages, 'max_tokens': 1000 if json_only else 300,
              **({'response_format': {'type': 'json_object'}} if json_only else {})},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']


def describe_error(error):
    """ Short description of a provider failure for the log. The providers explain errors in the response body
    (e.g. "model not found"), which is more useful than the status code alone. Never includes the API key,
    because the key is sent in a header, not in the URL or body. """
    response = getattr(error, 'response', None)
    if response is not None:
        return f"{response.status_code} {response.text[:200]}"
    return str(error)


# Matches each provider's name in PROVIDERS to the procedure that talks to it
ASK = {'gemini': ask_gemini, 'groq': ask_groq}


def ask_providers(history, system=SYSTEM_PROMPT, json_only=False):
    """ Try each provider in PROVIDERS in turn and return (answer text, provider name) from the first that answers.
    history must already be checked (clean_history). Also used by model/ai_theme.py with its own system prompt.
    Raises ChatError(503) if every provider was skipped or failed. """
    for provider in PROVIDERS:
        api_key = os.environ.get(provider['key_env'])
        if not api_key:
            continue  # no key in .env for this provider: skip it
        model = os.environ.get(provider['model_env']) or provider['default_model']
        try:
            reply = ASK[provider['name']](history, api_key, model, system, json_only).strip()
        except (requests.RequestException, KeyError, IndexError, ValueError) as error:
            # Log the real error for us (never the key), then fall through to the next provider.
            # flush=True writes it to the log file right away instead of holding it in memory.
            print(f"Chat: {provider['name']} failed: {describe_error(error)}", flush=True)
            continue
        if reply:
            print(f"Chat: answered by {provider['name']} ({model})", flush=True)
            return reply, provider['name']

    # Every provider was skipped or failed
    raise ChatError("The assistant isn't available right now. Please try again later or use the Contact page.", 503)


def get_reply(history):
    """ Answer the visitor's latest message.

    Parameter: history, the conversation so far: a list of {'role', 'content'} messages ending with the visitor's.
    Returns {'reply': text, 'provider': name of the service that answered}.
    Raises ChatError if the conversation is not allowed or no provider could answer.
    """
    # 1. Check the conversation first, so nothing bad or private is ever sent to an AI service
    history = clean_history(history)
    # 2. Try each provider in order and stop at the first good answer, so the chat keeps working if one is down
    reply, provider = ask_providers(history)
    return {'reply': reply, 'provider': provider}


def is_available():
    """ True if at least one provider has a key, so the frontend only shows the bubble when it can answer """
    return any(os.environ.get(provider['key_env']) for provider in PROVIDERS)
