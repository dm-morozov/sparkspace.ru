"""Homepage invitation to discuss a project through existing contact channels."""
from html import escape

import stage6
import stage9


def enquiry():
    contacts = {item[0]: item for item in stage6.CONTACTS}
    channels = []
    for key, name in [('telegram', 'Telegram'), ('max', 'MAX')]:
        href = escape(contacts[key][3], quote=True)
        channels.append(
            f'<a class="enquiry25-messenger" href="{href}" target="_blank" '
            f'rel="noopener noreferrer" aria-label="Обсудить проект в {name}">'
            f'{stage9.messenger_icon(key)}<span>Написать в {name}</span></a>'
        )
    phone = contacts['phone']
    email = contacts['email']
    return '''<section class="wrap enquiry25" aria-labelledby="enquiry25-title">
<div class="enquiry25-surface">
<div class="enquiry25-copy">
<span class="eyebrow">ОБСУДИМ ВАШ ПРОЕКТ</span>
<h2 id="enquiry25-title">Расскажите о задаче.<br>Предложим решение.</h2>
<p>Что хотите запустить или улучшить? Можно прислать ссылку на сайт или описать процесс, который занимает слишком много времени.</p>
<div class="enquiry25-result"><span>Обсудим подходящий вариант,<br>этапы и оценку стоимости.</span></div>
</div>
<div class="enquiry25-actions">
<img class="enquiry25-art" src="assets/stage25-enquiry-v1.jpg" width="720" height="480" loading="lazy" decoding="async" alt="">
<div class="enquiry25-messengers">''' + ''.join(channels) + '''</div>
<div class="enquiry25-secondary"><a href="''' + escape(phone[3], quote=True) + '''">''' + escape(phone[2]) + '''</a><a href="''' + escape(email[3], quote=True) + '''">''' + escape(email[2]) + '''</a></div>
</div>
</div>
</section>'''
