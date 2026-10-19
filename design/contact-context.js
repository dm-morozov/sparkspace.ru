/* A local message starter only: no form, API request, storage or auto-send. */
const serviceNames = {
 websites: 'Разработка сайтов', applications: 'Веб- и мобильные приложения',
 automation: 'Автоматизация бизнеса', integrations: 'Интеграции и онлайн-оплата',
 redesign: 'Редизайн сайта', seo: 'Продвижение сайтов', audit: 'Аудит сайта',
 support: 'Поддержка и развитие', unsure: 'Помощь с выбором решения'
};
const service = new URLSearchParams(location.search).get('service');
const context = document.querySelector('[data-contact-context]');
if (context && Object.hasOwn(serviceNames, service)) {
 const name = serviceNames[service];
 const message = `Здравствуйте! Хочу обсудить услугу «${name}».\n\nМоя задача: \nСайт (если есть): `;
 context.hidden = false;
 context.querySelector('[data-service-name]').textContent = name;
 const starter = context.querySelector('textarea');
 starter.value = message;
 const email = document.querySelector('.public-contact-list a[href^="mailto:"]');
 if (email) email.href = `mailto:dem.morozov@gmail.com?subject=${encodeURIComponent('SparkSpace: ' + name)}&body=${encodeURIComponent(message)}`;
 const button = context.querySelector('button');
 const status = context.querySelector('[role="status"]');
 button.addEventListener('click', async () => {
  try {
   await navigator.clipboard.writeText(starter.value);
   status.textContent = 'Текст скопирован. Вставьте его в удобный мессенджер.';
  } catch {
   starter.focus(); starter.select();
   status.textContent = 'Текст выделен. Скопируйте его вручную.';
  }
 });
}
