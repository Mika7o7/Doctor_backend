from django.db import models

from api.models import User


class Chat(models.Model):

    from_user = models.ForeignKey(
        User,
        related_name="sended",
        on_delete=models.CASCADE,
        verbose_name="Ուղարկող",
    )
    to_user = models.ForeignKey(
        User,
        related_name="received",
        on_delete=models.CASCADE,
        verbose_name="Ստացող",
    )
    text_massage = models.TextField("նամակ", blank=True, null=True)
    document = models.FileField(
        "Կցված ֆայլ", blank=True, null=True, upload_to=""
    )
    sended_time = models.DateTimeField("Ուղարկելու ժամ", auto_now_add=True)
    edited = models.BooleanField("Փոփոխված է", default=False)
    readed = models.BooleanField("Կարդացված է", default=False)

    class Meta:
        verbose_name = "նամակ"
        verbose_name_plural = "Նամակներ"

    def __str__(self) -> str:
        return f"{self.from_user.first_name} {self.to_user.first_name}"
