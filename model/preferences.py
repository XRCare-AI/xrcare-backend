""" User preferences: how the site looks and sounds for one user (same idea as Open Coding Society's
/api/user/preferences, which its pages repo's dashboard Preferences tab saves to).

Stored as JSON on the user (User._preferences). The frontend's Preferences page (/account/preferences/) edits them
and js/theme.js applies them on every page. This file defines what may be stored: DEFAULTS (the site as designed),
the allowed choices (FONTS, BUTTON_STYLES, LANGUAGES) and clean_preferences(), which checks a whole set from the
browser and returns it tidied up, or raises PreferencesError with a message for the user.
Keep FONTS, BUTTON_STYLES and LANGUAGES in step with the frontend's js/theme.js.
"""
import re


# The site as designed (dark navy, white text, cyan accent, Montserrat at 17px). A user with these values
# sees the site exactly as it was built, so the frontend skips repainting it.
DEFAULTS = {
    'theme': 'Site Default',   # name of the preset or saved theme last picked (only shown on the page)
    'bg': '#050a18',
    'text': '#ffffff',
    'accent': '#17ddfc',
    'selectionColor': '#17ddfc',
    'font': 'site',
    'size': 17,
    'buttonStyle': 'default',
    'language': '',
    'ttsVoice': '',
    'ttsRate': 1.0,
    'ttsPitch': 1.0,
    'ttsVolume': 1.0,
    'headTracking': {
        'enabled': False,
        'sensitivity': 0.45,
        'calibration': None,   # {centerX, centerY, leftX, rightX, upY, downY} once captured
    },
    'customThemes': {},
}

FONTS = ('site', 'inter', 'roboto', 'open-sans', 'lato', 'montserrat', 'atkinson', 'georgia', 'source-code-pro')
BUTTON_STYLES = ('default', 'rounded-all', 'square', 'pill')
LANGUAGES = ('', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'zh-CN', 'zh-TW', 'ja', 'ko', 'ar', 'hi', 'vi', 'th', 'nl',
             'pl', 'tr', 'uk', 'he', 'fa', 'tl')

SIZE_RANGE = (14, 24)          # px; the site's own body text is 17px
MAX_CUSTOM_THEMES = 10         # same limit as Open Coding Society
THEME_NAME_MAX = 30
THEME_FIELDS = ('bg', 'text', 'accent', 'selectionColor', 'font', 'size', 'buttonStyle')
CALIBRATION_FIELDS = ('centerX', 'centerY', 'leftX', 'rightX', 'upY', 'downY')

HEX_COLOR = re.compile(r'^#[0-9a-fA-F]{6}$')


class PreferencesError(ValueError):
    """ A preference the site cannot use; the message is safe to show the user """


def _color(value, label):
    if not isinstance(value, str) or not HEX_COLOR.match(value):
        raise PreferencesError(f"{label} must be a color like #1a2b3c.")
    return value.lower()


def _number(value, low, high, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PreferencesError(f"{label} must be a number.")
    if not low <= value <= high:
        raise PreferencesError(f"{label} must be between {low} and {high}.")
    return round(float(value), 3)


def _choice(value, allowed, label):
    if value not in allowed:
        raise PreferencesError(f"{label} is not one of the available choices.")
    return value


def _look(source, defaults):
    """ The appearance fields of a theme (colors, font, size, button style) """
    return {
        'bg': _color(source.get('bg', defaults['bg']), 'Background color'),
        'text': _color(source.get('text', defaults['text']), 'Text color'),
        'accent': _color(source.get('accent', defaults['accent']), 'Accent color'),
        'selectionColor': _color(source.get('selectionColor', defaults['selectionColor']), 'Selection color'),
        'font': _choice(source.get('font', defaults['font']), FONTS, 'Font'),
        'size': int(_number(source.get('size', defaults['size']), *SIZE_RANGE, 'Text size')),
        'buttonStyle': _choice(source.get('buttonStyle', defaults['buttonStyle']), BUTTON_STYLES, 'Button style'),
    }


def clean_preferences(prefs):
    """ Check a full set of preferences from the browser. Missing fields get their default.
    Returns the cleaned dict; raises PreferencesError if anything is not allowed. """
    if not isinstance(prefs, dict):
        raise PreferencesError("Send your preferences as an object.")

    cleaned = _look(prefs, DEFAULTS)

    theme = prefs.get('theme', DEFAULTS['theme'])
    if not isinstance(theme, str) or len(theme) > THEME_NAME_MAX:
        raise PreferencesError(f"Theme names can be up to {THEME_NAME_MAX} characters.")
    cleaned['theme'] = theme.strip()

    cleaned['language'] = _choice(prefs.get('language', ''), LANGUAGES, 'Language')

    voice = prefs.get('ttsVoice', '')
    if not isinstance(voice, str) or len(voice) > 200:
        raise PreferencesError("That voice name is too long.")
    cleaned['ttsVoice'] = voice
    cleaned['ttsRate'] = _number(prefs.get('ttsRate', 1.0), 0.5, 2, 'Speed')
    cleaned['ttsPitch'] = _number(prefs.get('ttsPitch', 1.0), 0.5, 2, 'Pitch')
    cleaned['ttsVolume'] = _number(prefs.get('ttsVolume', 1.0), 0, 1, 'Volume')

    tracking = prefs.get('headTracking') or {}
    if not isinstance(tracking, dict):
        raise PreferencesError("Head tracking settings could not be read.")
    calibration = tracking.get('calibration')
    if calibration is not None:
        if not isinstance(calibration, dict):
            raise PreferencesError("Head tracking calibration could not be read.")
        calibration = {key: _number(calibration.get(key), 0, 1, 'Calibration point') for key in CALIBRATION_FIELDS}
    cleaned['headTracking'] = {
        'enabled': bool(tracking.get('enabled', False)),
        'sensitivity': _number(tracking.get('sensitivity', 0.45), 0.1, 0.9, 'Sensitivity'),
        'calibration': calibration,
    }

    themes = prefs.get('customThemes') or {}
    if not isinstance(themes, dict):
        raise PreferencesError("Saved themes could not be read.")
    if len(themes) > MAX_CUSTOM_THEMES:
        raise PreferencesError(f"You can keep up to {MAX_CUSTOM_THEMES} themes. Delete one to add another.")
    cleaned['customThemes'] = {}
    for name, look in themes.items():
        name = str(name).strip()
        if not name or len(name) > THEME_NAME_MAX:
            raise PreferencesError(f"Theme names need 1 to {THEME_NAME_MAX} characters.")
        if not isinstance(look, dict):
            raise PreferencesError(f"The theme “{name}” could not be read.")
        cleaned['customThemes'][name] = _look(look, DEFAULTS)

    return cleaned
