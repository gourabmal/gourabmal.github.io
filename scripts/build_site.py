"""Generate a buildless portfolio, using the current Word CV as the content source."""
from pathlib import Path
from html import escape as e
from zipfile import ZipFile
from xml.etree import ElementTree as ET
import json

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://gourabmal.github.io/'
PAGES = []
LEGACY_URLS = {
    'project-1.html': 'high-quality-meats.html',
    'project-2.html': 'chips.html',
    'project-3.html': 'kenosis.html',
    'project-4.html': 'first-axis-capital.html',
}
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(ROOT / 'assets/docs/Gourab_Mal_CV.docx') as z:
    doc = ET.fromstring(z.read('word/document.xml'))
paragraphs = []
for p in doc.findall('.//w:body/w:p', NS):
    text = ''.join(p.itertext())
    style = p.find('w:pPr/w:pStyle', NS)
    paragraphs.append((text, style.get('{'+NS['w']+'}val') if style is not None else 'Normal'))
sections = {}
current = None
for text, style in paragraphs:
    if style == 'Section':
        current = text
        sections[current] = []
    elif current:
        sections[current].append((text, style))

def tags(items):
    return '<ul class="tags">'+''.join('<li>'+e(x)+'</li>' for x in items)+'</ul>'

def head(title, description, file):
    PAGES.append(file)
    url = BASE_URL + ('' if file == 'index.html' else file)
    page_title = f'{title} | Gourab Mal'
    if file == 'index.html':
        page_title = 'Gourab Mal | Senior Software Engineer · Laravel, PHP & Node.js'
    person = {
        '@type': 'Person', '@id': BASE_URL + '#gourab-mal',
        'name': 'Gourab Mal', 'url': BASE_URL,
        'jobTitle': 'Senior Software Engineer',
        'sameAs': ['https://github.com/gourabmal', 'https://www.linkedin.com/in/gourabmal/'],
        'knowsAbout': ['Laravel', 'PHP', 'Node.js', 'Vue.js', 'REST APIs', 'MySQL', 'AI integrations'],
    }
    page = {
        '@type': 'ProfilePage' if file in ['index.html', 'cv.html'] else 'WebPage',
        '@id': url + '#page', 'url': url, 'name': page_title,
        'description': description, 'inLanguage': 'en',
        'isPartOf': {'@id': BASE_URL + '#website'},
    }
    graph = [page]
    if file in ['index.html', 'cv.html']:
        page['mainEntity'] = {'@id': person['@id']}
        graph.append(person)
    else:
        page['author'] = {'@id': person['@id']}
    if file == 'index.html':
        graph.append({'@type': 'WebSite', '@id': BASE_URL + '#website', 'name': 'Gourab Mal', 'url': BASE_URL, 'publisher': {'@id': person['@id']}})
    elif file != 'thankyou.html':
        graph.append({'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Gourab Mal', 'item': BASE_URL},
            {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url},
        ]})
    structured_data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c')
    robots = 'noindex, follow' if file == 'thankyou.html' else 'index, follow, max-image-preview:large'
    return f'''<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(page_title)}</title><meta name="description" content="{e(description)}">
<meta name="author" content="Gourab Mal"><meta name="robots" content="{robots}">
<meta name="theme-color" content="#f8f7f3"><link rel="icon" href="favicon.ico" sizes="16x16 32x32 48x48">
<link rel="icon" type="image/png" sizes="96x96" href="assets/favicon/favicon-96.png"><link rel="icon" type="image/svg+xml" sizes="any" href="assets/favicon/favicon.svg">
<link rel="apple-touch-icon" sizes="180x180" href="assets/favicon/apple-touch-icon.png">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{e(page_title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Gourab Mal"><meta property="og:url" content="{url}"><meta property="og:locale" content="en_IN">
<meta property="og:image" content="{BASE_URL}assets/logo/social-preview.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Gourab Mal — Senior Software Engineer. Laravel, PHP, Node.js, Vue.js and AI integrations.">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(page_title)}"><meta name="twitter:description" content="{e(description)}"><meta name="twitter:image" content="{BASE_URL}assets/logo/social-preview.png"><meta name="twitter:image:alt" content="Gourab Mal — Senior Software Engineer">
<script type="application/ld+json">{structured_data}</script>
<link rel="stylesheet" href="css/portfolio.css"><script src="js/portfolio.js" defer></script></head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="shell header-inner">
<a class="brand" href="index.html" aria-label="Gourab Mal, home"><img class="brand-logo" src="assets/logo/gm-monogram.svg" width="44" height="44" alt=""><span class="brand-text">Gourab Mal<span>Senior Software Engineer</span></span></a>
<button class="menu-toggle" aria-controls="site-nav" aria-expanded="false">Menu <span aria-hidden="true">☰</span></button>
<nav id="site-nav" aria-label="Main navigation"><a href="index.html#work">Work</a><a href="index.html#skills">Skills</a><a href="index.html#experience">Experience</a><a href="index.html#about">About</a><a href="index.html#contact">Contact</a><a class="nav-cv" href="cv.html">View CV <span aria-hidden="true">↗</span></a></nav>
</div></header>'''

def footer():
    return '''<footer class="site-footer"><div class="shell footer-inner"><a class="footer-name" href="index.html">Gourab Mal<span>Software engineer. Curious by nature.</span></a><div><a href="https://github.com/gourabmal" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="https://www.linkedin.com/in/gourabmal/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="#main">Back to top ↑</a></div><small>© 2026 Gourab Mal</small></div></footer></body></html>'''

projects = [
    dict(file='high-quality-meats.html', name='High Quality Meats', category='E-commerce', filter='commerce', image='highqualitymeats.jpg', color='sage',
         intro='From product discovery to checkout.', description='An e-commerce platform with order management, payments, and a custom admin dashboard.',
         stack=['Laravel', 'MySQL', 'REST APIs', 'Payments'],
         overview='An e-commerce website for meat products, with product, category, order, and content management through an admin panel.',
         contributions=['Developed the e-commerce application and its admin features using Laravel.', 'Integrated online payments alongside a Cash on Delivery checkout option.', 'Worked on coupon management, tipping options, tax configuration, and notifications.']),
    dict(file='chips.html', name='CHIPS', category='E-commerce', filter='commerce', image='chips.jpg', color='sand',
         intro='The backend behind an electronics store.', description='Electronics commerce with inventory management, regional payments, and SMS notifications.',
         stack=['Laravel', 'MySQL', 'KNET', 'MyFatoorah'],
         overview='An electronics e-commerce application with products, categories, brands, stores, offers, and search. The website supports separate checkout flows for guests and registered customers.',
         contributions=['Worked on product and inventory functionality and optimized the MySQL schema.', 'Integrated KNET and MyFatoorah payments and SMS notifications.', 'Supported admin-managed homepage sections, coupon management, and tax configurations.']),
    dict(file='kenosis.html', name='Kenosis', category='Healthcare CMS', filter='cms', image='kenosis.jpg', color='blue',
         intro='Healthcare content, thoughtfully organized.', description='A CMS website for patient feedback, medical expert assessments, and healthcare information.',
         stack=['Laravel', 'PHP', 'CMS'],
         overview='A healthcare CMS website covering medical experts, hospitals, feedback, and assessments across Oncology, Haematology, Transplant, and Critical Care.',
         contributions=['Developed the CMS website for managing healthcare content and assessments.', 'Worked on admin-managed categories, subcategories, and informational content.', 'Added an enquiry form with CAPTCHA for visitors to contact the organization.']),
    dict(file='website-monitoring.html', name='Website Monitoring Tool', category='Automation', filter='automation', image='websitemonitoring.jpg', color='lavender',
         intro='Spot changes. Stay informed.', description='Automated screenshot comparison and alerts for visual changes across websites.',
         stack=['Node.js', 'Puppeteer', 'Alerts'],
         overview='A website monitoring tool that captures and compares screenshots to detect visual changes and send alerts.',
         contributions=['Used Node.js and Puppeteer to capture website screenshots.', 'Implemented screenshot comparisons to detect visual changes.', 'Added automated alerts to surface detected changes.']),
    dict(file='ai-article-generator.html', name='AI Article Generator & SEO Optimizer', category='AI integration', filter='automation', image=None, color='sage',
         intro='AI-assisted writing, inside WordPress.', description='A custom plugin bringing Claude-powered article generation and SEO suggestions into the WordPress dashboard.',
         stack=['WordPress', 'PHP', 'Claude API'],
         overview='A custom WordPress plugin that integrates Claude for article generation, keyword analysis, and SEO suggestions directly within the publishing workflow.',
         contributions=['Built the plugin using PHP and the Claude API.', 'Added article generation and keyword analysis within the WordPress dashboard.', 'Included SEO suggestions to support content editing.']),
    dict(file='first-axis-capital.html', name='First Axis Capital', category='Finance CMS', filter='cms', image='firstaxiscapital.jpg', color='sand',
         intro='A structured way to manage enquiries.', description='A CMS website with funding requests, partner onboarding forms, and centralized content management.',
         stack=['PHP', 'MySQL', 'JavaScript'],
         overview='A CMS-driven website that lets individuals and organizations submit funding requests and allows prospective ISO partners to register their interest.',
         contributions=['Developed the CMS website and structured funding request forms.', 'Added a dedicated form flow for ISO partner enquiries.', 'Implemented admin management for website content and submitted form data.'])
]

def project_visual(project, hero=False):
    if project['image']:
        return f'<img src="assets/jpg/{project["image"]}" alt="{e(project["name"])} website preview" loading="{"eager" if hero else "lazy"}" width="1280" height="769">'
    return '''<div class="writing-visual" aria-label="Illustration of an AI-assisted article workflow"><div class="editor-toolbar"><span></span><span></span><span></span><small>WORDPRESS × CLAUDE</small></div><div class="editor-paper"><span class="editor-label">IDEA → FIRST DRAFT</span><strong>A little inspiration.<br>A head start on writing.</strong><i></i><i></i><i></i><div class="editor-bottom"><span>Article generation</span><span>SEO suggestions</span></div></div></div>'''

cards = ''
for n, project in enumerate(projects):
    cards += f'''<article class="project-card" data-category="{project['filter']}"><a class="project-image {project['color']}" href="{project['file']}" aria-label="View {e(project['name'])} project">{project_visual(project)}<span class="project-open" aria-hidden="true">↗</span></a><div class="project-meta"><span>{project['category']}</span><span>0{n+1}</span></div><h3><a href="{project['file']}">{e(project['name'])}</a></h3><p>{project['description']}</p>{tags(project['stack'])}</article>'''

# Use the same skills inventory on the homepage and in the HTML CV.
portfolio_skills = [
    ('Backend & APIs', ['PHP', 'Laravel', 'Node.js', 'Express.js', 'REST APIs', 'WordPress', 'WooCommerce']),
    ('Frontend', ['Vue.js', 'Nuxt.js', 'JavaScript', 'HTML5', 'CSS3', 'Bootstrap', 'jQuery', 'AJAX']),
    ('Data & architecture', ['MySQL', 'MongoDB', 'Redis', 'SQL optimization', 'Multi-tenant SaaS', 'Microservices']),
    ('Real-time & security', ['Laravel Reverb', 'WebSockets', 'Role-based access control', 'Two-factor authentication']),
    ('AI & automation', ['Generative AI', 'AI agents', 'n8n', 'Claude', 'Gemini', 'RAG pipelines', 'Vector databases', 'MCP workflows', 'Prompt engineering']),
    ('Testing & delivery', ['Pest', 'Postman', 'Swagger / OpenAPI', 'Docker', 'Git', 'GitHub', 'Bitbucket', 'Sentry']),
    ('Tools & collaboration', ['Jira', 'Slack', 'ClickUp', 'Asana']),
    ('Platforms & CRMs', ['Lovable', 'CheckoutChamp', 'Konnektive', 'Sticky CRM', 'Vrio', '29Next', 'Klaviyo', 'Maropost']),
    ('Payment gateways', ['Stripe', 'PayPal', 'Razorpay', 'KNET', 'MyFatoorah']),
    ('Messaging & notifications', ['Twilio', 'AWS SES', 'Firebase Cloud Messaging (FCM)', 'SMS Gateway APIs', 'Telegram Bot API']),
]
skillrows = ''
for n, (name, items) in enumerate(portfolio_skills, start=1):
    skillrows += f'<div class="skill-row"><span class="row-number">{n:02d}</span><h3>{e(name)}</h3><p>{e(", ".join(items))}</p></div>'

experience = ''
all_jobs = sections['PROFESSIONAL EXPERIENCE'] + sections['PROFESSIONAL EXPERIENCE — CONTINUED']
jobs = []
for text, style in all_jobs:
    if style == 'Role': jobs.append({'role':text,'meta':'','bullets':[]})
    elif style == 'Meta': jobs[-1]['meta'] = text
    elif style == 'Bullet': jobs[-1]['bullets'].append(text.lstrip('• '))
for n, job in enumerate(jobs):
    role, company = job['role'].split(' | ',1)
    place, dates = job['meta'].split('  |  ',1)
    experience += f'''<article class="experience-row"><div class="experience-date"><span class="timeline-dot"></span><span>{e(dates)}</span><small>{e(place)}</small></div><div><h3>{e(company)}</h3><p class="job-role">{e(role)}</p><ul class="job-points">{''.join('<li>'+e(x)+'</li>' for x in job['bullets'])}</ul></div></article>'''

courses = ''
for text,_ in sections['CERTIFICATIONS & COURSES']:
    title, provider = text.rsplit(' – ',1)
    courses += f'<li><span>{e(title)}</span><small>{e(provider)}</small></li>'

main = head('Senior Software Engineer', 'Gourab Mal — 5+ years in web development, Laravel, PHP, Node.js, Vue.js, APIs, and AI integrations. Explore my work and experience.', 'index.html') + f'''
<main id="main">
<section class="hero shell" aria-labelledby="hero-title"><div class="hero-copy"><div class="availability"><span></span>Open to new opportunities</div><p class="eyebrow">GOURAB MAL · SENIOR SOFTWARE ENGINEER</p><h1 id="hero-title">Thoughtful code.<br><em>Useful products.</em></h1><p class="hero-description">I develop web applications, APIs, and AI-powered features that bring ideas into everyday use.</p><p class="hero-detail">5+ years of experience across Laravel, PHP, Node.js, and Vue.js projects. Based in West Bengal, India.</p><div class="hero-actions"><a class="button primary" href="#work">Explore my work <span aria-hidden="true">↓</span></a><a class="button text-button" href="assets/docs/Gourab_Mal_CV.pdf" download>Download CV <span aria-hidden="true">↗</span></a></div><div class="hero-social"><a href="https://github.com/gourabmal" target="_blank" rel="noopener noreferrer">GitHub ↗</a><span></span><a href="https://www.linkedin.com/in/gourabmal/" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a></div></div>
<div class="hero-art" aria-label="Areas of engineering experience"><span class="art-index">A LOOK UNDER THE HOOD</span><div class="art-grid"></div><div class="system-node node-ui"><span class="node-icon">&lt;/&gt;</span><div><small>THE INTERFACE</small><strong>Web applications</strong><p>Vue.js · JavaScript</p></div></div><div class="system-connector connector-one"></div><div class="system-node node-api"><span class="node-icon">&#123; &#125;</span><div><small>THE CONNECTION</small><strong>Backend & APIs</strong><p>Laravel · PHP · Node.js</p></div><span class="node-signal"></span></div><div class="system-connector connector-two"></div><div class="system-node node-data"><span class="node-icon">≋</span><div><small>THE FOUNDATION</small><strong>Data & integrations</strong><p>MySQL · MongoDB · AI</p></div></div><div class="art-caption"><span class="tiny-dot"></span>Different layers. One connected experience.</div></div></section>
<div class="stack-strip"><div class="shell"><span>MY EVERYDAY TOOLKIT</span><p>Laravel <i>·</i> PHP <i>·</i> Node.js <i>·</i> Vue.js <i>·</i> MySQL <i>·</i> n8n</p></div></div>
<section id="work" class="section shell"><div class="section-heading"><div><p class="eyebrow">01 / SELECTED WORK</p><h2>Ideas, brought<br>to the browser.</h2></div><p>A selection of web applications, integrations, and tools I’ve worked on. Explore the details behind each project.</p></div>
<div class="filters" role="group" aria-label="Filter projects"><button data-filter="all" aria-pressed="true">All work <span>06</span></button><button data-filter="commerce" aria-pressed="false">E-commerce</button><button data-filter="automation" aria-pressed="false">AI & automation</button><button data-filter="cms" aria-pressed="false">CMS websites</button></div><p class="sr-only" id="filter-status" aria-live="polite"></p><div class="project-grid">{cards}</div>
<aside class="lab-note"><span class="lab-label">FROM MY LAB <span>PERSONAL DEMO</span></span><div><h3>CartPilot AI</h3><p>An experiment in AI shopping assistance and human handoff using Laravel, n8n, Gemini, Supabase, and Telegram.</p></div><a href="cartpilot-demo.html" class="text-link">Explore the demo <span aria-hidden="true">↗</span></a></aside></section>
<section id="skills" class="section skills-section"><div class="shell"><div class="section-heading"><div><p class="eyebrow">02 / TECHNICAL SKILLS</p><h2>The tools behind<br>the work.</h2></div><p>Backend development at the core, with experience across frontend interfaces, data, and integrations.</p></div><div class="skill-list">{skillrows}</div></div></section>
<section id="experience" class="section shell"><div class="section-heading"><div><p class="eyebrow">03 / EXPERIENCE</p><h2>Where I’ve<br>made a contribution.</h2></div><a class="text-link" href="cv.html">View full CV ↗</a></div><div class="experience-list">{experience}</div></section>
<section id="about" class="section about-section"><div class="shell about-grid"><div class="about-title"><p class="eyebrow">04 / A LITTLE ABOUT ME</p><h2>An engineer.<br>A writer.<br><em>Always curious.</em></h2><div class="about-location"><span class="tiny-dot"></span>West Bengal, India</div></div><div class="about-copy"><p class="large-copy">I’m Gourab, a software engineer who enjoys understanding how things work—and making them work together.</p><p>Over the past five years, I’ve worked across e-commerce, healthcare, and travel applications. Most recently, I contributed to backend modules in an existing multi-tenant SaaS platform built with Laravel at Innofied Solutions.</p><p>Outside work, I write articles, explore new technologies, and enjoy creative writing through poems and stories.</p><div class="about-facts"><div><small>EDUCATION</small><h3>B.Tech, Computer Science & Engineering</h3><p>Mallabhum Institute of Technology<br>2020 · DGPA 8.81</p></div><div><small>LANGUAGES</small><p>English · Hindi · Bengali</p></div></div></div></div></section>
<section id="credentials" class="section shell"><div class="credentials-grid"><div><p class="eyebrow">05 / CONTINUOUS LEARNING</p><h2>Curiosity,<br>put into practice.</h2><p class="credentials-intro">Courses that complement my work in web development and AI integrations.</p><h3 class="awards-heading">Recognition</h3><ul class="award-list"><li><span>Promising Stars Empowering the Team</span><small>Swadesh Softwares · 2022</small></li><li><span>Lakshmi Narayana Memorial Award</span><small>Academic Topper · Mallabhum Institute of Technology · 2018</small></li></ul></div><div><h3 class="list-title">Certifications & courses</h3><ul class="course-list">{courses}</ul></div></div></section>
<section id="contact" class="contact-section"><div class="shell"><p class="eyebrow">HAVE A ROLE OR PROJECT IN MIND?</p><div class="contact-grid"><h2>Let’s make<br><em>something useful.</em></h2><div><p>I’m open to full-time and contract opportunities in web development, backend engineering, and AI integrations.</p><a class="contact-email" href="mailto:gourabmal4@gmail.com">gourabmal4@gmail.com <span aria-hidden="true">↗</span></a><div class="contact-actions"><button class="button copy-email" type="button">Copy email address</button><a href="https://www.linkedin.com/in/gourabmal/" target="_blank" rel="noopener noreferrer">Connect on LinkedIn ↗</a></div><p class="copy-status" role="status"></p></div></div></div></section>
</main>''' + footer()
(ROOT/'index.html').write_text(main)

for p in projects:
    content = head(f"{p['name']} — {p['category']} Project",p['description'],p['file']) + f'''<main id="main"><section class="case-hero shell"><a class="back-link" href="index.html#work">← Back to selected work</a><p class="eyebrow">{p['category']} / PROJECT OVERVIEW</p><h1>{e(p['name'])}</h1><p class="case-lede">{p['intro']}</p>{tags(p['stack'])}</section><div class="shell"><div class="case-image {p['color']}">{project_visual(p,True)}</div></div><section class="section shell case-content"><div><p class="eyebrow">THE PROJECT</p><h2>What it does.</h2><p>{p['overview']}</p></div><div><p class="eyebrow">MY CONTRIBUTION</p><h2>What I worked on.</h2><ul>{''.join('<li>'+x+'</li>' for x in p['contributions'])}</ul></div></section><div class="case-bottom shell"><a class="button primary" href="index.html#contact">Let’s talk about your project ↗</a><a class="text-link" href="index.html#work">More selected work →</a></div></main>''' + footer()
    (ROOT/p['file']).write_text(content)

# An accessible HTML CV and matching PDF/Word downloads share the same source.
resume = ''
in_list = False
active_section = ''
for text,style in paragraphs[5:]:
    if style != 'Bullet' and in_list:
        resume += '</ul>'
        in_list = False
    if style == 'Section':
        active_section = text.strip().casefold()
        resume += '<h2>'+e(text.title())+'</h2>'
        if active_section == 'technical skills':
            resume += ''.join(
                f'<p><strong>{e(name)}:</strong> {e(", ".join(items))}</p>'
                for name, items in portfolio_skills
            )
    elif style == 'Role': resume += '<h3>'+e(text)+'</h3>'
    elif style == 'Bullet':
        if not in_list: resume += '<ul>'; in_list = True
        resume += '<li>'+e(text.lstrip('• '))+'</li>'
    elif style == 'Skill':
        if active_section != 'technical skills':
            label,items = text.split(':',1)
            resume += '<p><strong>'+e(label)+':</strong>'+e(items)+'</p>'
    else: resume += '<p class="'+('resume-meta' if style == 'Meta' else '')+'">'+e(text)+'</p>'
if in_list: resume += '</ul>'
(ROOT/'cv.html').write_text(head('Curriculum Vitae','Gourab Mal — professional experience, technical skills, education, and courses. Download the latest CV.','cv.html')+f'''<main id="main" class="shell resume-page"><div class="resume-toolbar"><a class="back-link" href="index.html">← Back to portfolio</a><div><a class="button primary" href="assets/docs/Gourab_Mal_CV.pdf" download>Download PDF ↓</a><a class="button secondary" href="assets/docs/Gourab_Mal_CV.docx" download>Word version ↓</a></div></div><article class="resume-sheet"><h1>Gourab Mal</h1><p class="resume-role">Senior Software Engineer</p><p>West Bengal, India · +91 9064884148 · <a href="mailto:gourabmal4@gmail.com">gourabmal4@gmail.com</a></p><p><a href="https://www.linkedin.com/in/gourabmal/">LinkedIn</a> · <a href="https://github.com/gourabmal">GitHub</a> · <a href="index.html">Portfolio</a></p>{resume}</article></main>'''+footer())

demo = head('CartPilot AI — Personal Demo','A personal demo exploring AI shopping assistance and human handoff with Laravel, n8n, Gemini, Supabase, and Telegram.','cartpilot-demo.html')+'''
<main id="main"><section class="case-hero shell"><a class="back-link" href="index.html#work">← Back to portfolio</a><p class="eyebrow">FROM MY LAB / PERSONAL DEMO PROJECT</p><h1>CartPilot AI</h1><p class="case-lede">AI assistance.<br>A human when it matters.</p><p class="demo-intro">A personal demo exploring product discovery and customer support, with conversation handoff to a human agent on Telegram.</p>'''+tags(['Laravel','n8n','Gemini','Supabase','Telegram API'])+'''</section><div class="shell"><div class="video-placeholder" data-video="YwavwHf12zI"><p class="eyebrow">PROJECT WALKTHROUGH</p><h2>See the demo in action.</h2><button class="button primary load-video">Play video <span aria-hidden="true">▶</span></button><p>Loads a video from YouTube when you press play.</p><a href="https://www.youtube.com/watch?v=YwavwHf12zI" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a></div></div><section class="section shell case-content"><div><p class="eyebrow">THE EXPERIMENT</p><h2>Connecting AI<br>and human support.</h2><p>This demo combines a website chat interface, Gemini responses, and human handoff. It is a personal project exploring the integration flow.</p></div><div><p class="eyebrow">HOW THE DEMO WORKS</p><ol class="flow-list"><li>A customer sends a message through the chat widget.</li><li>An n8n workflow routes the request to Gemini.</li><li>Supabase broadcasts the response to the chat interface.</li><li>When a human is needed, the conversation moves to Telegram with its context.</li><li>AI responses pause while the human agent replies.</li></ol></div></section><div class="case-bottom shell"><a class="text-link" href="index.html#work">← Explore professional projects</a></div></main>'''+footer()
(ROOT/'cartpilot-demo.html').write_text(demo)
(ROOT/'thankyou.html').write_text(head('Get in touch','Contact Gourab Mal about software engineering roles and projects.','thankyou.html')+'''<main id="main" class="shell case-hero"><p class="eyebrow">GET IN TOUCH</p><h1>Let’s connect.</h1><p class="case-lede">Send your message directly by email.</p><a class="button primary" href="mailto:gourabmal4@gmail.com">Email Gourab ↗</a><p class="demo-intro">This page does not send messages automatically.</p><a class="text-link" href="index.html">← Back to portfolio</a></main>'''+footer())
print('Generated homepage, six project pages, demo, CV, and contact fallback.')

# GitHub Pages has no configurable server redirects; immediate HTML redirects
# preserve existing links while canonical URLs point to the descriptive pages.
for old, new in LEGACY_URLS.items():
    (ROOT / old).write_text(f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Project moved | Gourab Mal</title><link rel="canonical" href="{BASE_URL}{new}">
<meta http-equiv="refresh" content="0;url={new}"></head>
<body><p>This project has moved. <a href="{new}">View the project</a>.</p></body></html>''')

sitemap = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for file in dict.fromkeys(PAGES):
    if file == 'thankyou.html':
        continue
    entry = ET.SubElement(sitemap, 'url')
    ET.SubElement(entry, 'loc').text = BASE_URL + ('' if file == 'index.html' else file)
ET.ElementTree(sitemap).write(ROOT / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE_URL + 'sitemap.xml\n')
(ROOT / '.nojekyll').touch()
print('Generated legacy redirects, canonical sitemap, and robots.txt.')
