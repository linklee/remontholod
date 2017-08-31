# coding=utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import email.mime.application
import os

# Settings
smtp = 'smtp.gmail.com'
smtp_port = 587
login = 'nevernight721'
password = '9022774182'

def send_mail(_from, _to, subject, html, file=None, path=None):
    if _from is None or _to is None or subject is None or html is None:
        return False
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = _to
    msgHtml = MIMEText(html, 'html', _charset='utf-8')
    msg.attach(msgHtml)

    if path is not None and file is not None:
        try:
            fp = open(path + file, 'rb')
            att = email.mime.application.MIMEApplication(fp.read(), _subtype="doc")
            fp.close()
            att.add_header('Content-Disposition', 'attachment', filename=file)
            msg.attach(att)
        except IOError:
            return False

    server = smtplib.SMTP(smtp, smtp_port)
    server.starttls()
    server.login(login, password)
    server.sendmail(_from, _to, msg.as_string())
    server.quit()
    return True

def send_message(to, message):
    send_mail(login, to, 'Вы оставили заявку', message)

def send_message_self(message):
    send_mail(login, 'nevernight721@gmail.com', 'Новая заявка', message)
    send_mail(login, 'info@optimagp.ru"', 'Новая заявка', message)