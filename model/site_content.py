""" Seed content for the site, copied word for word from xrcare.ai (data only; model/site.py loads it)

Image paths are files in the frontend repo (images/).
Text that may hold formatting (bios, quotes) is HTML limited to <b> <strong> <em> <i> <br> <a>;
the frontend removes anything else.

Section layouts (js/page.js in the frontend draws each one):
  spotlight     Home intro over a background video
                {title, slogan, highlight, links: [{label, url, icon}], badge: {image, alt}, video: {src, poster}}
  copilot       The animated co-pilot graphic beside a paragraph (may hold <strong>)  {text, core_label, inputs: [{icon, label}]}
  capabilities  Capability explorer (auto-cycles)  {heading, items: [{icon, title, text}]}
  pillars       Cards lit one after another        {heading_accent, heading, items: [{icon, title, text}]}
  audiences     Linked audience tiles              {heading, link_label, items: [{icon, title, text, url}]}
  cta           Call to action band                {heading, text, primary: {label, url}, secondary}
  pagehead      Top of a page                      {title, highlight, text}
  subnav        Sticky links to the page's sections {links: [{label, url, icon}]}
  audience      One audience on Explore            {heading, text, image, reverse, features: [{icon, title, text}], cta}
  articles      Searchable article list            {heading, text, search_placeholder, all_label, read_more, no_results}
  about         About Us intro                     {heading, highlight, text, columns: [{icon, title, text}], quote: {image, text, author, role}}
  team          Team bios                          {read_bio, hide_bio, groups: [{heading, members: [{image, name, title, bio: [html]}]}]}
  (icon is a Font Awesome 6 class list, e.g. "fa-solid fa-eye")
A heading given as a list is shown with a line break between the parts.
"""

SETTINGS = {
    'site_title': 'XRCare AI',
    'logo': '/images/logo.png',
    'linkedin_url': 'https://www.linkedin.com/company/xrcare/about/',
    'menu_label': 'Menu',
    'contact_heading': 'Ready to Transform Your Care Team?',
    'phone': '+1-858-324-4114',
    'phone_href': 'tel:+18583244114',
    'email': 'info@XRCare.ai',
    'footer_linkedin_url': 'https://www.linkedin.com/company/xrcare',
    'footer_background': '/images/darkhexes.jpg',
    'header_background': '/images/darkhexes.jpg',
    'copyright': '© 2026 Plerion AI, Inc. All rights reserved. XRCare™ is a DBA of Plerion AI, Inc.',
    'contact_submit_label': 'Submit',
    'contact_sending_label': 'Sending...',
    'not_found': {'title': 'Page not found', 'code': '404', 'heading': 'Page Not Found',
                  'button': {'label': 'Back Home', 'url': '/'}},
    'blog': {
        'title': 'Articles',
        'by': 'By',
        'read_more': 'Read More',
        'search_placeholder': 'Search...',
        'recent_posts': 'Recent Posts',
        'archives': 'Archives',
        'categories': 'Categories',
        'meta': 'Meta',
        'log_in': 'Log in',
        'popular_posts': 'Popular Posts',
        'previous_post': 'Previous Post',
        'next_post': 'Next Post',
        'share': 'Share',
        'home': 'Home',
        'no_results': 'Nothing Found',
        'no_results_text': 'Sorry, but nothing matched your search terms. Please try again with some different keywords.',
        'results_for': 'Results For',
        'category_label': 'Category',
        'author_label': 'Author',
        'archive_label': 'Archive',
    },
    'login': {
        'title': 'Log in',
        'heading': 'Log in',
        'username_label': 'Username or Email',
        'password_label': 'Password',
        'submit_label': 'Log In',
        'logged_in_as': 'Logged in as',
        'log_out_label': 'Log Out',
        'admin_label': 'Admin',
        'user_label': 'User',
    },
    'account': {
        'log_in': 'Log in',
        'sign_up': 'Get Started',
        'log_out': 'Log out',
        'my_hub': 'My Hub',
        'admin_label': 'Admin',
    },
    'hub': {
        'title': 'My Hub',
        'greeting': 'Welcome back, {name}',
        'member_since': 'Member since {date}',
        'recommended': 'Recommended for you',
        'answers_button': 'Update my answers',
        'answers_heading': 'Your answers',
        'retake_survey': 'Retake the survey',
        'close': 'Close',
        'take_survey': 'Take the 1-minute survey',
        'explore_heading': 'Jump back in',
        'for_you': 'For you',
        'account_heading': 'Account',
        'edit': 'Edit',
        'save': 'Save changes',
        'cancel': 'Cancel',
        'saved': 'Saved.',
        'username_locked': 'This account’s username can’t be changed.',
        'name_label': 'Name',
        'username_label': 'Username',
        'email_label': 'Email',
        'role_label': 'Account type',
        'tiles': [
            {'key': 'clinical', 'icon': 'fa-solid fa-user-doctor', 'label': 'Clinical Teams',
             'text': 'Point-of-care guidance, faster onboarding, less admin.', 'url': '/explore/#clinical-teams'},
            {'key': 'training', 'icon': 'fa-solid fa-people-group', 'label': 'Care Team Training',
             'text': 'Collaborative XR scenarios with AI feedback.', 'url': '/explore/#care-team-training'},
            {'key': 'pharmacy', 'icon': 'fa-solid fa-prescription-bottle-medical', 'label': 'Pharmacy',
             'text': 'Fewer medication errors, smoother workflows.', 'url': '/explore/#pharmacy'},
            {'key': 'research', 'icon': 'fa-solid fa-newspaper', 'label': 'Articles',
             'text': 'Insights on XR, AI and the future of care.', 'url': '/explore/#articles'},
            {'key': 'exploring', 'icon': 'fa-solid fa-people-line', 'label': 'About Us',
             'text': 'Meet the team behind XRCare.', 'url': '/about-us/'},
            {'key': 'evaluating', 'icon': 'fa-solid fa-envelope', 'label': 'Contact',
             'text': 'Book a conversation with our team.', 'url': '/contact/'},
        ],
    },
    'auth': {
        'panel_heading': 'Care teams, amplified.',
        'panel_text': 'Immersive XR practice and a proactive AI co-pilot, built for the people who deliver care.',
        'panel_points': ['Zero-risk skill practice', 'AI coaching that adapts to you', 'Privacy-first by design'],
        'login_subheading': 'Welcome back. Log in to continue.',
        'no_account': 'Don’t have an account?',
        'sign_up_link': 'Sign up here',
        'show_password': 'Show password',
        'hide_password': 'Hide password',
        'continue_label': 'Continue',
    },
    'signup': {
        'title': 'Sign up',
        'heading': 'Create your account',
        'subheading': 'It takes less than a minute.',
        'name_label': 'Full Name',
        'username_label': 'Username',
        'username_hint': '3-40 letters, numbers, dots, dashes or underscores',
        'email_label': 'Email',
        'password_label': 'Password',
        'password_hint': 'At least 6 characters',
        'confirm_label': 'Confirm Password',
        'submit_label': 'Create Account',
        'password_mismatch': 'Passwords do not match',
        'have_account': 'Already have an account?',
        'log_in_link': 'Log in',
        'strength': ['Too short', 'Weak', 'Okay', 'Strong', 'Very strong'],
    },
    'survey': {
        'title': 'Welcome',
        'heading': 'Let’s tailor XRCare to you',
        'greeting': 'Hi {name}!',
        'intro': 'Six quick questions so we can show you what matters most.',
        'start_label': 'Start',
        'skip_label': 'Skip for now',
        'back_label': 'Back',
        'next_label': 'Next',
        'finish_label': 'Finish',
        'saving_label': 'Saving...',
        'step_label': 'Question {n} of {total}',
        'choose_up_to': 'Choose up to {max}',
        'key_hint': 'Tip: press a letter key to choose',
        'done_heading': 'You’re all set, {name}!',
        'done_text': 'Based on your answers, here’s the best place to start.',
        'done_secondary': {'label': 'Go to My Hub', 'url': '/account/'},
        'questions': [
            {
                'id': 'purpose', 'title': 'What brings you to XRCare?',
                'text': 'Pick the one that fits best.',
                'options': [
                    {'id': 'clinical', 'icon': 'fa-solid fa-user-doctor', 'label': 'Support for my clinical team',
                     'recommend': {'label': 'Explore XRCare for Clinical Teams', 'url': '/explore/#clinical-teams'}},
                    {'id': 'training', 'icon': 'fa-solid fa-people-group', 'label': 'Care team training',
                     'recommend': {'label': 'Explore Care Team Training', 'url': '/explore/#care-team-training'}},
                    {'id': 'pharmacy', 'icon': 'fa-solid fa-prescription-bottle-medical',
                     'label': 'Pharmacy workflows & safety',
                     'recommend': {'label': 'See XRCare for Pharmacy', 'url': '/explore/#pharmacy'}},
                    {'id': 'evaluating', 'icon': 'fa-solid fa-building', 'label': 'Evaluating XRCare for my organization',
                     'recommend': {'label': 'Book a conversation with our team', 'url': '/contact/'}},
                    {'id': 'research', 'icon': 'fa-solid fa-flask', 'label': 'Research or education',
                     'recommend': {'label': 'Read our latest articles', 'url': '/explore/#articles'}},
                    {'id': 'exploring', 'icon': 'fa-solid fa-compass', 'label': 'Just exploring',
                     'recommend': {'label': 'Meet the team behind XRCare', 'url': '/about-us/'}},
                ],
            },
            {
                'id': 'role', 'title': 'Which best describes your role?',
                'options': [
                    {'id': 'nurse', 'icon': 'fa-solid fa-user-nurse', 'label': 'Nurse'},
                    {'id': 'physician', 'icon': 'fa-solid fa-stethoscope', 'label': 'Physician / APP'},
                    {'id': 'pharmacist', 'icon': 'fa-solid fa-pills', 'label': 'Pharmacist / Pharmacy tech'},
                    {'id': 'educator', 'icon': 'fa-solid fa-chalkboard-user', 'label': 'Clinical educator / Trainer'},
                    {'id': 'leader', 'icon': 'fa-solid fa-briefcase', 'label': 'Healthcare leader / Administrator'},
                    {'id': 'it', 'icon': 'fa-solid fa-microchip', 'label': 'IT / Innovation'},
                    {'id': 'student', 'icon': 'fa-solid fa-graduation-cap', 'label': 'Student'},
                    {'id': 'other', 'icon': 'fa-solid fa-ellipsis', 'label': 'Other'},
                ],
            },
            {
                'id': 'setting', 'title': 'Where do you work?',
                'options': [
                    {'id': 'hospital', 'icon': 'fa-solid fa-hospital', 'label': 'Hospital / Emergency Dept.'},
                    {'id': 'inpatient', 'icon': 'fa-solid fa-bed-pulse', 'label': 'Med-surg / Inpatient unit'},
                    {'id': 'ltc', 'icon': 'fa-solid fa-house-medical', 'label': 'Long-term care'},
                    {'id': 'home_health', 'icon': 'fa-solid fa-house-user', 'label': 'Home health'},
                    {'id': 'pharmacy', 'icon': 'fa-solid fa-mortar-pestle', 'label': 'Pharmacy'},
                    {'id': 'clinic', 'icon': 'fa-solid fa-clinic-medical', 'label': 'Clinic / Outpatient'},
                    {'id': 'academic', 'icon': 'fa-solid fa-building-columns', 'label': 'School / Training program'},
                    {'id': 'other', 'icon': 'fa-solid fa-ellipsis', 'label': 'Other'},
                ],
            },
            {
                'id': 'goals', 'title': 'What would you most like to improve?', 'multiple': True, 'max': 3,
                'options': [
                    {'id': 'admin_burden', 'icon': 'fa-solid fa-file-pen', 'label': 'Less documentation & admin work'},
                    {'id': 'onboarding', 'icon': 'fa-solid fa-rocket', 'label': 'Faster training & onboarding'},
                    {'id': 'med_errors', 'icon': 'fa-solid fa-triangle-exclamation', 'label': 'Fewer medication errors'},
                    {'id': 'teamwork', 'icon': 'fa-solid fa-comments', 'label': 'Team communication & coordination'},
                    {'id': 'burnout', 'icon': 'fa-solid fa-battery-half', 'label': 'Less burnout & cognitive load'},
                    {'id': 'skills', 'icon': 'fa-solid fa-hand-holding-medical', 'label': 'Safe practice of high-risk skills'},
                ],
            },
            {
                'id': 'xr_experience', 'title': 'How familiar are you with XR (VR / AR)?',
                'options': [
                    {'id': 'none', 'icon': 'fa-solid fa-seedling', 'label': 'Never tried it'},
                    {'id': 'tried', 'icon': 'fa-solid fa-vr-cardboard', 'label': 'Tried it once or twice'},
                    {'id': 'occasional', 'icon': 'fa-solid fa-vr-cardboard', 'label': 'Use it occasionally'},
                    {'id': 'regular', 'icon': 'fa-solid fa-bolt', 'label': 'Use it regularly'},
                ],
            },
            {
                'id': 'team_size', 'title': 'How large is the team you’re thinking about?',
                'options': [
                    {'id': 'solo', 'icon': 'fa-solid fa-user', 'label': 'Just me'},
                    {'id': 'small', 'icon': 'fa-solid fa-user-group', 'label': '2-10 people'},
                    {'id': 'medium', 'icon': 'fa-solid fa-users', 'label': '11-50 people'},
                    {'id': 'large', 'icon': 'fa-solid fa-users-line', 'label': '51-250 people'},
                    {'id': 'enterprise', 'icon': 'fa-solid fa-city', 'label': 'More than 250'},
                ],
            },
        ],
    },
}

NAV = [
    ('Home', '/'),
    ('About Us', '/about-us/'),
    ('Explore', '/explore/'),
    ('Contact', '/contact/'),
]

# Home page (redesigned in content version 2: no stock photos; motion graphics drawn by the frontend)
HOME = {
    'slug': 'home', 'title': 'Home',
    'sections': [
        {
            'slug': 'intro', 'name': 'XR AI Care Co-Pilot', 'layout': 'spotlight', 'theme': 'light',
            'content': {
                'title': 'XR-AI Care Co-Pilot™',
                'slogan': 'Delivering the Power of XR + AI to Healthcare',
                'highlight': 'XR + AI',
                'links': [
                    {'label': 'Get Started', 'url': '/signup/', 'icon': 'fa-solid fa-rocket'},
                    {'label': 'About Us', 'url': '/about-us/', 'icon': 'fa-solid fa-people-group'},
                    {'label': 'Explore XRCare', 'url': '/explore/', 'icon': 'fa-solid fa-compass'},
                    {'label': 'Contact', 'url': '/contact/', 'icon': 'fa-solid fa-envelope'},
                ],
                'badge': {'image': '/images/evonexus.png', 'alt': 'EvoNexus Portfolio Company'},
                # Photos from the site crossfading with a slow zoom (frontend tools/make-hero-reel.py)
                'video': {'src': '/videos/hero-reel.mp4', 'poster': '/videos/hero-reel.jpg'},
            },
        },
        {
            'slug': 'co-pilot', 'name': 'The Co-Pilot', 'layout': 'copilot', 'theme': 'dark',
            'content': {
                'text': 'The XR-AI Co-Pilot <strong>revolutionizing the future of healthcare</strong> for clinical '
                        'teams, pharmacies and care team training. The XR platform that delivers AI aimed at '
                        '<strong>improving patient care</strong> experiences.',
                'core_label': 'Care Co-Pilot',
                'inputs': [
                    {'icon': 'fa-solid fa-eye', 'label': 'Vision'},
                    {'icon': 'fa-solid fa-microphone-lines', 'label': 'Speech'},
                    {'icon': 'fa-solid fa-heart-pulse', 'label': 'Sensors'},
                    {'icon': 'fa-solid fa-file-medical', 'label': 'EMR'},
                ],
            },
        },
        {
            'slug': 'features', 'name': 'Agentic AI Features', 'layout': 'capabilities', 'theme': 'dark',
            'content': {
                'heading': 'Empower Your Care Teams with a Trusted Co-Pilot',
                'items': [
                    {'icon': 'fa-solid fa-eye', 'title': 'Context-Aware Intelligence',
                     'text': 'Understands every care moment through real-time visual, audio, and workflow cues.'},
                    {'icon': 'fa-solid fa-wand-magic-sparkles', 'title': 'Proactive Co-Pilot',
                     'text': 'Anticipates clinician needs, surfacing next-best actions before errors occur.'},
                    {'icon': 'fa-solid fa-layer-group', 'title': 'Multimodal Insight',
                     'text': 'Combines vision, speech, sensor, and EMR data for complete context.'},
                    {'icon': 'fa-solid fa-diagram-project', 'title': 'Adaptive Orchestration',
                     'text': 'Unites AI agents to streamline documentation, decisions, and safety.'},
                    {'icon': 'fa-solid fa-arrows-rotate', 'title': 'Continuous Learning',
                     'text': 'Improves performance and workflows with every interaction.'},
                    {'icon': 'fa-solid fa-shield-halved', 'title': 'Privacy-First Design',
                     'text': 'Built on consent, minimal data use, and secure, compliant operations.'},
                ],
            },
        },
        {
            'slug': 'Avoid-Burnout', 'name': 'Modern Solutions', 'layout': 'pillars', 'theme': 'light',
            'content': {
                'heading_accent': 'Avoid Burnout:',
                'heading': 'Modern Solutions for Real-World Challenges',
                'items': [
                    {'icon': 'fa-solid fa-gauge-high', 'title': 'Improve Efficiency',
                     'text': 'Smarter workflows and real-time AI support mean tasks take less time. From medication '
                             'dispensing to bedside care, your team can work faster without sacrificing quality.'},
                    {'icon': 'fa-solid fa-vr-cardboard', 'title': 'Enhance Work Capabilities',
                     'text': 'XR immerses clinicians in lifelike scenarios while AI provides personalized coaching. '
                             'Together, they expand professional skills, confidence and adaptability for critical '
                             'situations.'},
                    {'icon': 'fa-solid fa-brain', 'title': 'Reduce Errors, Lighten Cognitive Load',
                     'text': 'AI catches risks before they become mistakes, and XR practice can reduce stress under '
                             'pressure. The result: fewer errors, sharper focus and better decision-making.'},
                ],
            },
        },
        {
            'slug': 'Critical-areas-of-impact', 'name': 'Critical Areas of Impact', 'layout': 'audiences', 'theme': 'dark',
            'content': {
                'heading': 'Critical Areas of Impact',
                'link_label': 'Explore',
                'items': [
                    {'icon': 'fa-solid fa-user-doctor', 'title': 'Clinical Teams', 'url': '/explore/#clinical-teams',
                     'text': 'Immersive XR patient simulations with AI coaching can accelerate onboarding and sharpen '
                             'critical thinking in emergency and bedside care. Personalized AI tracking builds '
                             'confidence, boosts retention and adapts learning to the needs of each clinician.'},
                    {'icon': 'fa-solid fa-prescription-bottle-medical', 'title': 'Pharmacy', 'url': '/explore/#pharmacy',
                     'text': 'AI-driven XR simulations help pharmacists reduce medication errors and allows '
                             'individuals and teams to optimize workflows.'},
                    {'icon': 'fa-solid fa-people-group', 'title': 'Care Team Training',
                     'url': '/explore/#care-team-training',
                     'text': 'Team-based XR scenarios mirror real patient challenges, breaking down silos and '
                             'improving collaboration. AI feedback enhances communication and coordination while '
                             'scalable training supports hospitals, clinics and networks.'},
                ],
            },
        },
        {
            'slug': 'get-started', 'name': 'Get Started', 'layout': 'cta', 'theme': 'light',
            'content': {
                'heading': 'See what a co-pilot can do for your team',
                'primary': {'label': 'Create an Account', 'url': '/signup/'},
                'secondary': {'label': 'Log In', 'url': '/login/'},
            },
        },
    ],
}

# Explore: one hub for the audiences (formerly For Clinical Teams / For Care Team Training) and the articles
EXPLORE = {
    'slug': 'explore', 'title': 'Explore',
    'sections': [
        {
            'slug': 'top', 'name': 'Explore', 'layout': 'pagehead', 'theme': 'dark',
            'content': {
                'title': 'Explore XRCare',
                'highlight': 'XRCare',
                'text': 'Everything in one place: how the XR-AI Co-Pilot supports clinical teams, care team '
                        'training and pharmacy, plus our latest articles.',
            },
        },
        {
            'slug': 'jump', 'name': '', 'layout': 'subnav', 'theme': 'dark',
            'content': {'links': [
                {'label': 'Clinical Teams', 'url': '#clinical-teams', 'icon': 'fa-solid fa-user-doctor'},
                {'label': 'Care Team Training', 'url': '#care-team-training', 'icon': 'fa-solid fa-people-group'},
                {'label': 'Pharmacy', 'url': '#pharmacy', 'icon': 'fa-solid fa-prescription-bottle-medical'},
                {'label': 'Articles', 'url': '#articles', 'icon': 'fa-solid fa-newspaper'},
            ]},
        },
        {
            'slug': 'clinical-teams', 'name': 'Clinical Teams', 'layout': 'audience', 'theme': 'dark',
            'content': {
                'title': 'For Clinical Teams',
                'heading': 'Delivering the Power of XR + AI to Clinical Teams',
                'text': 'The frontline solution is here: XR Care for Clinical Teams delivers less admin load, more '
                        'patient time, better training and Point-of-care guidance, leading to safer, higher-quality '
                        'patient outcomes.',
                'image': '/images/clinical-teams.jpg',
                'features': [
                    {'icon': 'fa-solid fa-graduation-cap', 'title': 'Accelerate Training & Onboarding',
                     'text': 'Interactive XR simulations speed up readiness in ED, med-surg, LTC, and home health.'},
                    {'icon': 'fa-solid fa-heart-pulse', 'title': 'Zero-Risk Skill Practice',
                     'text': 'Practice procedures safely before applying them to real patients.'},
                    {'icon': 'fa-solid fa-file-medical', 'title': 'Reduce Administrative Burden',
                     'text': 'AI-assisted charting, coding, and reporting free nurses for patient care.'},
                ],
                'cta': {'label': 'Talk to Our Team', 'url': '/contact/'},
            },
        },
        {
            'slug': 'care-team-training', 'name': 'Care Team Training', 'layout': 'audience', 'theme': 'dark',
            'content': {
                'title': 'For Care Team Training',
                'heading': 'Delivering the Power of XR + AI to Care Team Training',
                'text': 'Where AI Meets Learning: Building confidence through collaborative team scenarios, advancing '
                        'skills with consistent, AI-driven modules, and supporting growth with personalized '
                        'analytics—all designed to empower care teams to support peak-level performance.',
                'image': '/images/care-team-training.jpg',
                'reverse': True,
                'features': [
                    {'icon': 'fa-solid fa-people-arrows', 'title': 'Collaborative Learning',
                     'text': 'XR team scenarios improve coordination and reduce errors in handoffs.'},
                    {'icon': 'fa-solid fa-scale-balanced', 'title': 'Consistent Standards',
                     'text': 'AI modules ensure training consistency across sites and staff levels.'},
                    {'icon': 'fa-solid fa-chart-line', 'title': 'Continuous Improvement',
                     'text': 'Analytics reveal gaps and guide personalized skill development.'},
                ],
                'cta': {'label': 'Talk to Our Team', 'url': '/contact/'},
            },
        },
        {
            'slug': 'pharmacy', 'name': 'Pharmacy', 'layout': 'audience', 'theme': 'dark',
            'content': {
                'title': 'For Pharmacy',
                'heading': 'Delivering the Power of XR + AI to Pharmacy',
                'text': 'AI-driven XR simulations help pharmacists reduce medication errors and allows individuals '
                        'and teams to optimize workflows.',
                'image': '/images/pharmacy.jpg',
                'cta': {'label': 'Talk to Our Team', 'url': '/contact/'},
            },
        },
        {
            'slug': 'articles', 'name': 'Articles', 'layout': 'articles', 'theme': 'dark',
            'content': {
                'heading': 'Articles',
                'text': 'Insights from the XRCare team on XR, AI and the future of care.',
                'search_placeholder': 'Search articles',
                'all_label': 'All',
                'read_more': 'Read article',
                'no_results': 'No articles match your search.',
            },
        },
    ],
}


def member(image, name, title, *bio):
    return {'image': f'/images/team/{image}.png', 'name': name, 'title': title, 'bio': list(bio)}


ABOUT = {
    'slug': 'about-us', 'title': 'About Us',
    'sections': [
        {
            'slug': 'built-for-experts', 'name': 'Built by Industry Experts', 'layout': 'about', 'theme': 'dark',
            'content': {
                'heading': 'Built for Experts by Experts',
                'highlight': 'Experts',
                'text': 'One of the industry’s top executive teams in engineering and innovation have converged to '
                        'deliver the best XR-AI platform for the future of healthcare.',
                'columns': [
                    {'title': 'Vision', 'icon': 'fa-solid fa-binoculars',
                     'text': 'Deliver XR-AI solution as an end-to-end XR-AI solution serving as a Point-of-Care  '
                             'Co-pilot™ streamlining documentation, accelerating workflows and boosting accuracy for '
                             'clinical teams, pharmacies and care team training.'},
                    {'title': 'Mission', 'icon': 'fa-solid fa-flag',
                     'text': 'To build the most sought-after trusted intelligent XR-AI platform that redefines '
                             'human‐environment interactions – starting in healthcare and scaling the ecosystem to '
                             'support sectors including: education, industrial, public safety and more.'},
                ],
                'quote': {
                    'image': '/images/team/amin-barhoush.png',
                    'text': '“XR-AI Point-of-Care Co-Pilot is becoming the new standard for every clinician, '
                            'pharmacist and care team trainer, empowering them to work smarter, reduce errors and '
                            'unlock capabilities we could only imagine a few years ago.”',
                    'author': 'Amin Barhoush',
                    'role': 'Founder of XR Care',
                },
            },
        },
        {
            'slug': 'team', 'name': 'Our Team', 'layout': 'team', 'theme': 'dark',
            'content': {'read_bio': 'Read bio', 'hide_bio': 'Hide bio', 'groups': [
                {'heading': 'Executive Team', 'members': [
                    member('amin-barhoush', 'AMIN BARHOUSH', 'CEO',
                           '<b>Amin Barhoush</b> is the Chief Executive Officer of Plerion AI, Inc., where he leads the '
                           'development of the XRCare platform with a steadfast vision to revolutionize healthcare '
                           'through the immersive XR-AI Co-pilot. An engineer at heart and a program manager by '
                           'discipline, Amin brings more than 25 years of experience spanning product and systems '
                           'engineering.',
                           'Prior to founding XRCare.ai, Amin held senior leadership roles across diverse industries. '
                           'Most notably, he directed software development for Qualcomm’s application processors. '
                           'Earlier, he contributed to a nationwide healthcare digital transformation initiative in '
                           'Qatar for the FIFA 2022 World Cup.',
                           'Amin combines deep technical fluency with sharp business acumen—positioning XRCare.ai at '
                           'the forefront of the XR-AI healthcare transformation. He holds an M.B.A. from the '
                           'University of Scranton, an M.S. in wireless communication from National University, and a '
                           'B.E.T. in electronics from the University of Toledo.'),
                    member('quyen-ly', 'QUYEN LY, MBA, R.Ph.', 'CO-FOUNDER &amp; CPO',
                           '<b>Quyen Ly, MBA, R.Ph.</b>, is a strategic advisor and leader specializing in Digital '
                           'Health, AI-driven analytics, and clinical informatics platforms. With a unique blend of '
                           'Oncology Pharmacy expertise and business acumen, she helps early-stage companies bridge '
                           'transformative technology with market viability.',
                           'Her operational leadership across major healthcare systems evolved from clinical practice '
                           'into high-impact IT leadership, where she implemented large-scale IoT initiatives, '
                           'including Infusion InterOp and Medical Device Integration with Cerner EMR systems. At '
                           'Becton Dickinson, she guided AI-driven analytics platforms and defined enterprise data '
                           'strategy. As Global Head of Service at Philips HealthCare, her strategic direction led the '
                           'business to achieve positive EBITA for the first time, demonstrating strong capabilities '
                           'in P&amp;L management and global cloud migration.',
                           'Beyond her executive roles, Quyen mentors future professionals as a Preceptor at UCSD '
                           'Skaggs School of Pharmacy and holds leadership roles with the Asian Pacific Healthcare '
                           'Foundation and Van Lang Center San Diego.'),
                    member('haider-ali', 'DR HAIDER ALI', 'CTO, Agentic-AI',
                           '<b>Haider Ali, Ph.D.,</b> has more than 15 years of experience in computer vision and '
                           'artificial intelligence across Asia, Europe, and the U.S. Dr. Ali is the founder and CEO '
                           'of Crowdception Inc. He previously served as an assistant research professor of computer '
                           'science at Johns Hopkins University and as a senior research scientist at the German '
                           'Aerospace Center (DLR).',
                           'Dr. Ali earned his Ph.D. in computer science from Vienna University of Technology, '
                           'Austria, in 2010, and has since driven innovation in AI, automation, and health systems.'),
                    member('yasser-alsaied', 'YASSER ALSAIED', 'Executive Advisor',
                           '<strong>Yasser Alsaied</strong> is the Executive Advisor to the XRCare management team, '
                           'guiding strategic direction and technology innovation. With over 30 years of leadership in '
                           'AI, IoT, and cloud computing—including as Global VP of IoT at Amazon Web Services (AWS) and '
                           'as a senior executive at Qualcomm—Yasser brings deep expertise in scaling intelligent '
                           'platforms and connecting advanced systems from edge to cloud. At XRcare, he helps shape the '
                           'vision of redefining clinical precision through AI-driven extended reality, integrating '
                           'real-time intelligence into clinical workflows to enhance provider confidence, procedural '
                           'accuracy, and patient outcomes.'),
                ]},
                {'heading': 'Clinical Advisors', 'members': [
                    member('preetham-suresh', 'DR PREETHAM SURESH, MD', 'Clinical Advisor',
                           '<b>Dr. Preetham Suresh, MD, </b>is a Clinical Advisor and practicing anesthesiologist with '
                           'over 20 years of experience at the intersection of medicine and technology. With a '
                           'clinical focus on ultrasound-guided peripheral nerve blocks, he brings a rare combination '
                           'of engineering rigor and medical expertise, grounded in a BS in Chemical Engineering from '
                           'Northwestern University and a Doctor of Medicine from Case Western Reserve University.',
                           'At UC San Diego Health, Dr. Suresh serves as Clinical Professor of Anesthesiology and Vice '
                           'Chair of Innovation and Entrepreneurship, championing the integration of emerging '
                           'technology into clinical practice. As Associate Dean for Medical Education in Simulation '
                           'and Medical Director of UCSD’s Simulation Training Center, he designs forward-thinking '
                           'educational programs that cultivate innovation across healthcare. He also serves as a '
                           'Staff Anesthesiologist at the VA San Diego Healthcare System and as a Board Examiner for '
                           'the American Board of Anesthesiology.',
                           'His background in chemical engineering has fueled collaboration on medical device and '
                           'pharmaceutical development projects, making him a uniquely effective bridge between '
                           'clinical insight and technological innovation.'),
                    member('michael-becker', 'DR MICHAEL BECKER', 'Nursing Advisor',
                           '<b>Michael Becker, Ph.D., R.N.,</b> is a nationally recognized healthcare executive and '
                           'nursing leader with more than two decades of experience driving innovation at the '
                           'intersection of clinical practice and technology. He served as chief nursing officer at '
                           'Penn Presbyterian Medical Center, leading quality and safety advancements, and as vice '
                           'president of nursing and chief nursing executive at Masimo, where he shaped global '
                           'clinical strategy and AI-enabled monitoring solutions.',
                           'As executive strategic advisor, Dr. Becker helps guide the company’s vision, ensuring '
                           'innovation translates into measurable clinical and operational value.'),
                    member('pamela-wiltfang', 'DR. PAMELA WILTFANG', 'Pharmacy Advisor',
                           '<strong>Pamela Wiltfang, Pharm.D., M.P.H.</strong>, is an adjunct assistant professor at '
                           'the University of Iowa College of Pharmacy and Kirkwood Community College, where she '
                           'developed curricula in pharmacology, pharmaceutical calculations and compounding, pharmacy '
                           'operations and regulations, and pharmacy law.',
                           'Her career includes roles as Rare Disease Medical Science Liaison at Amgen, Associate '
                           'Director of Oncology and Immunology Medical Science Liaison at Immunocore, and Director of '
                           'Clinical Services and Innovative Practice at NuCara Health Solutions. She also served as '
                           'pharmacist-in-charge for more than 10 pharmacies, managing over 50 employees directly and '
                           'more than 500 indirectly across 30 sites in the Midwest.',
                           'Pamela’s experience spans Iowa, Illinois, Minnesota, Kansas, Missouri, Wisconsin, '
                           'Nebraska, North Dakota, South Dakota, and Texas, and includes collaboration with PBMs and '
                           'payers such as Wellmark, TriStar, and ACOs.'),
                ]},
                {'heading': 'Technical Advisors', 'members': [
                    member('irfan-khan', 'DR IRFAN KHAN', 'System Architect/ ML Advisor',
                           '<b>Irfan Khan, Ph.D., </b>has been a technology executive with deep expertise in system '
                           'solutions, ASICs, cellular infrastructure, communication networks and AI. Over his 30-year '
                           'past career at Qualcomm, Ericsson, and SRI International, he has driven groundbreaking '
                           'innovations and led the commercialization of several flagship products. He has '
                           'successfully built and scaled high-performance global R&amp;D teams from the ground up. '
                           'For the past several years, Dr. Khan has delved into AI/ML topics. Leveraging his strong '
                           'math background and hardware/software knowledge, he has developed a deep understanding of '
                           'AI models, their applicability for various use cases, key performance metrics and '
                           'performance enhancing techniques. He has taught machine learning at university level. Dr. '
                           'Khan is a co-inventor on several issued patents.',
                           'Dr. Khan is active in San Diego’s startup ecosystem, serving as an angel investor and '
                           'advisor. He is a member of NuFund Venture Group. Passionate about giving back, he is a '
                           'mentor for the Alaska gBETA accelerator and is an adjunct faculty member at San Diego '
                           'State University (SDSU) and UC San Diego (UCSD), where he teaches machine learning and '
                           'data science courses. He also serves as Chair of the Computer Science Industry Advisory '
                           'Board (IAB) at SDSU.',
                           'Dr. Khan holds a Ph.D. in Electrical Engineering from the University of Southern '
                           'California (USC), and MS degrees in Electrical Engineering (George Washington University) '
                           'and Computer Science (USC). He also earned an MBA in Entrepreneurship from SDSU and a B.E. '
                           'in Electrical &amp; Electronics Engineering from BITS Pilani, India.'),
                    member('ammar-darkazanli', 'AMMAR DARKAZANLI', 'Regulatory Advisor',
                           '<b>Ammar Darkazanli, Ph.D., M.B.A.,</b> is a transformational technology leader with more '
                           'than 20 years of experience architecting scalable healthcare platforms and driving AI/VR '
                           'innovation in clinical care. He currently leads platform architecture for an immersive '
                           'XR-AI co-pilot revolutionizing healthcare delivery.',
                           'Previously, he served as CEO/CTO of Ocu Health Care and held executive roles at '
                           'Biofourmis, Shifamed, Cala Health, and Glooko. Ammar’s expertise spans AI/ML platform '
                           'development, healthcare regulatory compliance (including FDA, HIPAA, SOC 2, ISO 13485, and '
                           'IEC 62304), cloud-native architectures, EMR integration, and global team leadership.',
                           'He holds an M.B.A. from the NYU Stern School of Business and a Ph.D. in electrical and '
                           'computer engineering from the University of Arizona.'),
                    member('khaled-el-maleh', 'DR KHALED EL-MALEH', 'Innovation Advisor',
                           '<b>Khaled El-Maleh, Ph.D.,</b> worked as a senior director of technology in the IP '
                           'department at Qualcomm, leading the AI/ML IP Portfolio Team in key innovation areas '
                           'including 5G/6G, distributed learning, AI acceleration, generative modeling, and '
                           'multimedia. He was the engineering lead for the multimedia, software, position location, '
                           'and sensors IP teams. In his role, he led IP acquisition, litigation, and strategy '
                           'development.',
                           'Dr. El-Maleh received bachelor’s degrees in electrical engineering and applied mathematics '
                           'from KFUPM in Saudi Arabia, and M.S., Eng., and Ph.D. degrees in electrical and computer '
                           'engineering from McGill University, Canada. He is an accomplished inventor with more than '
                           '400 U.S. and international patents.'),
                ]},
            ]},
        },
    ],
}

CONTACT = {
    'slug': 'contact', 'title': 'Contact',
    'sections': [{
        'slug': 'top', 'name': 'Contact', 'layout': 'pagehead', 'theme': 'dark',
        'content': {
            'title': 'Contact Us',
            'text': 'Call, email or send us a message below and the XRCare team will get back to you.',
        },
    }],
}

# Bump CONTENT_VERSION and list the page slugs in RESEED to replace those pages in existing databases
# (admin edits to them are lost; settings are only ever added, never replaced)
CONTENT_VERSION = 6
RESEED = {2: ['home'], 3: ['home'],
          4: ['home', 'about-us', 'contact', 'for-clinicalteams', 'care-team-training'],  # the last two became Explore
          5: ['home'], 6: []}
# Settings whose seed changed: replaced in existing databases at that version
RESEED_SETTINGS = {4: ['account', 'survey'], 5: ['hub'], 6: ['hub']}
# Versions at which the menu is replaced with NAV
RESEED_NAV = {4}

PAGES = [HOME, ABOUT, EXPLORE, CONTACT]
