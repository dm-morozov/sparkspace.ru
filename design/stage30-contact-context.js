/* Optional enquiry context. No requests, storage, tracking, or automatic sending. */
(() => {
  const root = document.querySelector('[data-contact-context]');
  if (!root) return;
  const services = {
    websites: 'Разработка сайта',
    applications: 'Разработка приложения',
    automation: 'Автоматизация бизнеса',
    integrations: 'Интеграция сервисов',
    redesign: 'Редизайн сайта',
    seo: 'Продвижение сайта',
    audit: 'Проверка или аудит сайта',
    support: 'Доработка и поддержка сайта'
  };
  const scenarios = {
    sales: {service: 'automation', label: 'Заявки и продажи'},
    commerce: {service: 'integrations', label: 'Торговля'},
    auto: {service: 'automation', label: 'Автосервис'},
    property: {service: 'automation', label: 'Управляющая компания'},
    content: {service: 'automation', label: 'Контент и публикации'}
  };
  const formats = {landing: 'Лендинг', company: 'Сайт компании', shop: 'Интернет-магазин'};
  const params = new URLSearchParams(window.location.search);
  const serviceKey = params.get('service');
  const service = Object.prototype.hasOwnProperty.call(services, serviceKey) ? services[serviceKey] : '';
  const formatKey = params.get('format');
  const format = serviceKey === 'websites' && Object.prototype.hasOwnProperty.call(formats, formatKey) ? formats[formatKey] : '';
  const scenarioKey = params.get('scenario');
  const candidate = Object.prototype.hasOwnProperty.call(scenarios, scenarioKey) ? scenarios[scenarioKey] : null;
  const scenario = service && candidate && candidate.service === serviceKey ? candidate.label : '';
  const selection = root.querySelector('[data-contact-selection]');
  const message = root.querySelector('[data-contact-message]');
  const button = root.querySelector('[data-contact-copy]');
  const status = root.querySelector('[data-contact-status]');
  if (!selection || !message || !button || !status) return;
  const topic = service ? service + (format ? ' · ' + format : '') + (scenario ? ' · ' + scenario : '') : '';
  selection.textContent = topic ? 'Вы выбрали: ' + topic : 'Можно начать с нескольких слов о вашей задаче.';
  const publicText = topic ? 'Здравствуйте! Хочу обсудить: ' + topic + '.' : 'Здравствуйте! Хочу обсудить проект.';
  message.value = publicText + '\n\nЗадача: ';
  // The email link contains only whitelisted public context, never the edited draft.
  const email = document.querySelector('.company29-contacts a[href^="mailto:"]');
  if (email && topic) {
    const address = email.getAttribute('href').split('?')[0];
    email.setAttribute('href', address + '?subject=' + encodeURIComponent('SparkSpace: ' + topic) +
      '&body=' + encodeURIComponent(publicText));
  }
  message.addEventListener('input', () => { status.textContent = ''; });
  let inFlight = false;
  button.addEventListener('click', async () => {
    if (inFlight) return;
    const text = message.value.trim();
    if (!text) {
      status.textContent = 'Добавьте несколько слов о задаче.';
      message.focus();
      return;
    }
    inFlight = true;
    button.setAttribute('aria-disabled', 'true');
    try {
      if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(text);
      status.textContent = 'Скопировано. Вставьте текст в выбранный мессенджер.';
    } catch {
      message.focus();
      message.select();
      status.textContent = 'Автоматически скопировать не удалось. Текст выделен — скопируйте его вручную.';
    } finally {
      inFlight = false;
      button.setAttribute('aria-disabled', 'false');
    }
  });
  root.hidden = false;
})();
