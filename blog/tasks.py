from celery import shared_task

from django.core.mail import send_mail


@shared_task
def new_comment(subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email='admin@example.com',
        recipient_list=['admin@example.com'],
        fail_silently=False
    )


@shared_task
def new_post(subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email='admin@example.com',
        recipient_list=['admin@example.com'],
        fail_silently=False
    )


@shared_task
def comment_active(subject, author, message):
    send_mail(
        subject=subject,
        message=message,
        from_email='admin@example.com',
        recipient_list=['admin@example.com', author],
        fail_silently=False
    )


@shared_task
def send_contact(subject, email, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=email,
        recipient_list=['admin@example.com'],
        fail_silently=False
    )
