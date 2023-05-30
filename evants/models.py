from django.db import models
from api.models import Doctor


class Evants(models.Model):

    date = models.DateField()
    time = models.TimeField()
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="evants",
        verbose_name="Բժիշկ",
    )

    class Meta:
        verbose_name = "Ժամանակացույց"
        verbose_name_plural = "Ժամանակացույցներ"

    def __str__(self) -> str:
        return f"{self.date} - {self.time}"
