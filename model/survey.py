""" First-login survey: the questions (which define what answers are stored) and the check for a set of answers.

The frontend's survey screens and My Hub read the questions from GET /api/survey; their wording around the
questions lives in the frontend (_data/site.yml, "survey").
Each question: {id, title, text?, multiple?, max?, options: [{id, icon, label, recommend?: {label, url}}]}
("recommend" on a purpose option is the page My Hub suggests for it.)
"""

QUESTIONS = [{'id': 'purpose',
  'title': 'What brings you to XRCare?',
  'text': 'Pick the one that fits best.',
  'options': [{'id': 'clinical',
               'icon': 'fa-solid fa-user-doctor',
               'label': 'Support for my clinical team',
               'recommend': {'label': 'Explore XRCare for Clinical Teams', 'url': '/explore/#clinical-teams'}},
              {'id': 'training',
               'icon': 'fa-solid fa-people-group',
               'label': 'Care team training',
               'recommend': {'label': 'Explore Care Team Training', 'url': '/explore/#care-team-training'}},
              {'id': 'pharmacy',
               'icon': 'fa-solid fa-prescription-bottle-medical',
               'label': 'Pharmacy workflows & safety',
               'recommend': {'label': 'See XRCare for Pharmacy', 'url': '/explore/#pharmacy'}},
              {'id': 'evaluating',
               'icon': 'fa-solid fa-building',
               'label': 'Evaluating XRCare for my organization',
               'recommend': {'label': 'Book a conversation with our team', 'url': '/contact/'}},
              {'id': 'research',
               'icon': 'fa-solid fa-flask',
               'label': 'Research or education',
               'recommend': {'label': 'Read our latest articles', 'url': '/explore/#articles'}},
              {'id': 'exploring',
               'icon': 'fa-solid fa-compass',
               'label': 'Just exploring',
               'recommend': {'label': 'Meet the team behind XRCare', 'url': '/about-us/'}}]},
 {'id': 'role',
  'title': 'Which best describes your role?',
  'options': [{'id': 'nurse', 'icon': 'fa-solid fa-user-nurse', 'label': 'Nurse'},
              {'id': 'physician', 'icon': 'fa-solid fa-stethoscope', 'label': 'Physician / APP'},
              {'id': 'pharmacist', 'icon': 'fa-solid fa-pills', 'label': 'Pharmacist / Pharmacy tech'},
              {'id': 'educator', 'icon': 'fa-solid fa-chalkboard-user', 'label': 'Clinical educator / Trainer'},
              {'id': 'leader', 'icon': 'fa-solid fa-briefcase', 'label': 'Healthcare leader / Administrator'},
              {'id': 'it', 'icon': 'fa-solid fa-microchip', 'label': 'IT / Innovation'},
              {'id': 'student', 'icon': 'fa-solid fa-graduation-cap', 'label': 'Student'},
              {'id': 'other', 'icon': 'fa-solid fa-ellipsis', 'label': 'Other'}]},
 {'id': 'setting',
  'title': 'Where do you work?',
  'options': [{'id': 'hospital', 'icon': 'fa-solid fa-hospital', 'label': 'Hospital / Emergency Dept.'},
              {'id': 'inpatient', 'icon': 'fa-solid fa-bed-pulse', 'label': 'Med-surg / Inpatient unit'},
              {'id': 'ltc', 'icon': 'fa-solid fa-house-medical', 'label': 'Long-term care'},
              {'id': 'home_health', 'icon': 'fa-solid fa-house-user', 'label': 'Home health'},
              {'id': 'pharmacy', 'icon': 'fa-solid fa-mortar-pestle', 'label': 'Pharmacy'},
              {'id': 'clinic', 'icon': 'fa-solid fa-clinic-medical', 'label': 'Clinic / Outpatient'},
              {'id': 'academic', 'icon': 'fa-solid fa-building-columns', 'label': 'School / Training program'},
              {'id': 'other', 'icon': 'fa-solid fa-ellipsis', 'label': 'Other'}]},
 {'id': 'goals',
  'title': 'What would you most like to improve?',
  'multiple': True,
  'max': 3,
  'options': [{'id': 'admin_burden', 'icon': 'fa-solid fa-file-pen', 'label': 'Less documentation & admin work'},
              {'id': 'onboarding', 'icon': 'fa-solid fa-rocket', 'label': 'Faster training & onboarding'},
              {'id': 'med_errors', 'icon': 'fa-solid fa-triangle-exclamation', 'label': 'Fewer medication errors'},
              {'id': 'teamwork', 'icon': 'fa-solid fa-comments', 'label': 'Team communication & coordination'},
              {'id': 'burnout', 'icon': 'fa-solid fa-battery-half', 'label': 'Less burnout & cognitive load'},
              {'id': 'skills',
               'icon': 'fa-solid fa-hand-holding-medical',
               'label': 'Safe practice of high-risk skills'}]},
 {'id': 'xr_experience',
  'title': 'How familiar are you with XR (VR / AR)?',
  'options': [{'id': 'none', 'icon': 'fa-solid fa-seedling', 'label': 'Never tried it'},
              {'id': 'tried', 'icon': 'fa-solid fa-vr-cardboard', 'label': 'Tried it once or twice'},
              {'id': 'occasional', 'icon': 'fa-solid fa-vr-cardboard', 'label': 'Use it occasionally'},
              {'id': 'regular', 'icon': 'fa-solid fa-bolt', 'label': 'Use it regularly'}]},
 {'id': 'team_size',
  'title': 'How large is the team you’re thinking about?',
  'options': [{'id': 'solo', 'icon': 'fa-solid fa-user', 'label': 'Just me'},
              {'id': 'small', 'icon': 'fa-solid fa-user-group', 'label': '2-10 people'},
              {'id': 'medium', 'icon': 'fa-solid fa-users', 'label': '11-50 people'},
              {'id': 'large', 'icon': 'fa-solid fa-users-line', 'label': '51-250 people'},
              {'id': 'enterprise', 'icon': 'fa-solid fa-city', 'label': 'More than 250'}]}]


def validate_survey(answers):
    """ Every question needs a valid answer: one option id, or a list of ids for multiple-choice questions.
    Returns an error message, or None """
    for question in QUESTIONS:
        options = {option['id'] for option in question['options']}
        answer = answers.get(question['id'])
        if question.get('multiple'):
            limit = question.get('max') or len(options)
            if not isinstance(answer, list) or not answer or not set(answer) <= options or len(set(answer)) > limit:
                return f"Please answer: {question['title']}"
        elif answer not in options:
            return f"Please answer: {question['title']}"
    unknown = set(answers) - {question['id'] for question in QUESTIONS}
    if unknown:
        return f"Unknown question: {sorted(unknown)[0]}"
    return None
