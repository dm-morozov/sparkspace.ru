"""Six truthful share-card briefs and their public-page mapping.

Image paths are output contracts, not a claim that images already exist.
Case artwork must use the specified real screenshot, never a generated UI.
Render title/subtitle/caption as typography; source art is a separate layer.
"""

SOCIAL_CARDS = {
    'general': {
        'image': 'assets/stage35-social-general.jpg',
        'title': 'Сайты, приложения и автоматизация',
        'subtitle': 'От задачи бизнеса — к цифровому решению.',
        'art': 'assets/stage27-hero-v1.png',
        'caption': '',
        'alt': 'SparkSpace: сайты, приложения и автоматизация бизнеса.',
    },
    'websites': {
        'image': 'assets/stage35-social-websites.jpg',
        'title': 'Сайты для вашего бизнеса',
        'subtitle': 'Лендинги, сайты компаний и интернет-магазины.',
        'art': 'assets/stage28-websites-v1.png',
        'caption': '',
        'alt': 'SparkSpace: разработка лендингов, сайтов компаний и интернет-магазинов.',
    },
    'systems': {
        'image': 'assets/stage35-social-systems.jpg',
        'title': 'Приложения и рабочие процессы',
        'subtitle': 'Сервисы для клиентов, команды и обмена данными.',
        'art': 'assets/stage27-process-cutout.png',
        'caption': '',
        'alt': 'SparkSpace: приложения, автоматизация и интеграция сервисов.',
    },
    'development': {
        'image': 'assets/stage35-social-development.jpg',
        'title': 'Развиваем действующий сайт',
        'subtitle': 'Аудит, редизайн, продвижение и сопровождение.',
        'art': 'assets/stage26-enquiry-cutout-v1.png',
        'caption': '',
        'alt': 'SparkSpace: аудит, редизайн, SEO и поддержка действующего сайта.',
    },
    'mu56': {
        'image': 'assets/stage35-social-mu56.jpg',
        'title': 'Мир Улыбок',
        'subtitle': 'Сайт собственного бизнеса детских праздников.',
        'art': 'assets/mu56-home-desktop.jpg',
        'caption': 'Реальный экран mu56.ru · 11.10.2026',
        'alt': 'Кейс SparkSpace «Мир Улыбок»: настоящий экран сайта детских праздников.',
    },
    'pilotspace': {
        'image': 'assets/stage35-social-pilotspace.jpg',
        'title': 'PilotSpace',
        'subtitle': 'Тренажёр по запросу пилотов из Узбекистана.',
        'art': 'assets/pilotspace-quiz-desktop.jpg',
        'caption': 'Реальный экран pilotspace.ru · 11.10.2026',
        'alt': 'Кейс SparkSpace PilotSpace: настоящий экран самостоятельного веб-тренажёра для пилотов.',
    },
}

PAGE_CARDS = {
    'index.html': 'general',
    'services.html': 'general',
    'websites.html': 'websites',
    'applications.html': 'systems',
    'automation.html': 'systems',
    'integrations.html': 'systems',
    'redesign.html': 'development',
    'seo.html': 'development',
    'audit.html': 'development',
    'support.html': 'development',
    'solutions.html': 'systems',
    'projects.html': 'general',
    'case-mu56.html': 'mu56',
    'case-pilotspace.html': 'pilotspace',
    'about.html': 'general',
    'approach.html': 'general',
    'prices.html': 'general',
    'contacts.html': 'general',
}
