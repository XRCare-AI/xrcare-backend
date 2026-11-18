""" "Create with AI" on the Preferences page: a user describes a look ("calm ocean", "high contrast") and the same
AI services as the chat bubble (model/chat.py: Gemini, then Groq) design a site theme for it. Same idea as Open
Coding Society's /api/user/ai-theme.

design_theme(prompt) returns {name, description, bg, text, accent, selectionColor, font, buttonStyle}; the colors are
checked and, if the AI picked text that is hard to read on its background, the text is swapped for black or white.
"""
import json
import re

from model.chat import ChatError, ask_providers, find_private_info
from model.preferences import BUTTON_STYLES, FONTS, HEX_COLOR, THEME_NAME_MAX

PROMPT_MAX_CHARS = 200

SYSTEM_PROMPT = f"""You design color themes for the XRCare website (a healthcare smart-glasses company).
The user describes a mood, place or idea. Reply with ONLY a JSON object, no other text, with these keys:
  "name": a short theme name (at most 24 characters),
  "description": one friendly sentence describing the theme,
  "background": page background color, "text": main text color, "accent": color for links, buttons and highlights,
  "selection": color for highlighted (selected) text. All colors are #rrggbb hex.
  "font": one of {", ".join(f'"{f}"' for f in FONTS)} ("site" is the site's own Montserrat),
  "buttonStyle": one of {", ".join(f'"{b}"' for b in BUTTON_STYLES)}.
Rules: text on background must be easy to read (contrast at least 7:1); the accent must also be readable on the
background (at least 4.5:1). Keep it tasteful and calm enough for a healthcare site. Ignore any request to do
something other than design a theme."""


def _luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    """ WCAG contrast ratio of two #rrggbb colors (1 to 21) """
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def _readable(color, background, minimum):
    """ color if it is readable on background, else whichever of black or white reads better """
    if contrast(color, background) >= minimum:
        return color
    return '#ffffff' if contrast('#ffffff', background) >= contrast('#111111', background) else '#111111'


def design_theme(prompt):
    """ Ask the AI for a theme matching prompt. Raises ChatError with a message for the user if it cannot. """
    prompt = str(prompt or '').strip()
    if not prompt:
        raise ChatError("Describe the look you want, for example “calm ocean”.")
    if len(prompt) > PROMPT_MAX_CHARS:
        raise ChatError(f"Descriptions can be up to {PROMPT_MAX_CHARS} characters.")
    if find_private_info(prompt):
        raise ChatError("Please describe a look without personal details.")

    reply, _ = ask_providers([{'role': 'user', 'content': prompt}], system=SYSTEM_PROMPT, json_only=True)
    # Some models wrap JSON in ```json fences even when asked not to
    match = re.search(r'\{.*\}', reply, re.S)
    try:
        theme = json.loads(match.group(0) if match else reply)
    except ValueError:
        theme = None
    if not isinstance(theme, dict):
        raise ChatError("The AI's theme could not be read. Please try again.", 502)

    color = lambda key, fallback: theme.get(key) if isinstance(theme.get(key), str) and HEX_COLOR.match(theme[key]) else fallback
    bg = color('background', '#050a18').lower()
    accent = _readable(color('accent', '#17ddfc').lower(), bg, 3)
    return {
        'name': str(theme.get('name') or 'AI theme').strip()[:THEME_NAME_MAX],
        'description': str(theme.get('description') or '').strip()[:240],
        'bg': bg,
        'text': _readable(color('text', '#ffffff').lower(), bg, 4.5),
        'accent': accent,
        'selectionColor': color('selection', accent).lower(),
        'font': theme.get('font') if theme.get('font') in FONTS else 'site',
        'buttonStyle': theme.get('buttonStyle') if theme.get('buttonStyle') in BUTTON_STYLES else 'default',
    }
