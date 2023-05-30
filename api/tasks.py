from celery import shared_task
from django.core.mail import send_mail

from my_doctor.settings import settings_base
from my_doctor.utils import encode_to_base64, encode_to_md5


@shared_task(bind=True)
def send_email_funq(
    self, user_id: int, user_email: str, user_date_joined: str
) -> str:
    decode_md5_data = encode_to_md5(user_email, user_date_joined)
    token_for_email = encode_to_base64(
        user_id=user_id,
        md5_data=decode_md5_data,
    )

    mail_subject = "Hi from Celery"
    message = f"Hello it's your token for login.\
             http://0.0.0.0:8000/activate/{token_for_email}"

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=settings_base.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
    return "message sent"


@shared_task()
def hello() -> str:
    return "Hello Mika"
