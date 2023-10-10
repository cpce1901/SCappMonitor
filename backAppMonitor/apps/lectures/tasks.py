from celery import shared_task
from django.core.mail import send_mail
from  apps.alerts.models import EmailNotifications


@shared_task(name="alert_email")
def send_email_alert(msg):
    emails_direction  = EmailNotifications.objects.all()
    subject = "Alerta Energia"
    message = msg
    from_email = "ircd.claudio@gmail.com"
    recipient_list = [i.email for i in emails_direction]

    send_mail(subject, message, from_email, recipient_list)

    return "send email"
