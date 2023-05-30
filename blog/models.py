from django.db import models
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django_resized import ResizedImageField


class Category(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "կատեգորիա"
        verbose_name_plural = "Կատեգորիաներ"


class Article(models.Model):
    title = models.CharField("Վերնագիր", max_length=200)
    created_at = models.DateTimeField("Գրանցման օր/ժամ", auto_now_add=True)
    image = ResizedImageField("Նկար", upload_to="BlogImage")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name="Կատեգորիա",
    )
    content = models.TextField("տեքստ")

    def __str__(self) -> str:
        return self.title

    def description_hy(self):
        return (
            Truncator(strip_tags(self.content_hy)).words(10, truncate=" ...")
            if self.content_hy
            else None
        )

    def description_ru(self):
        return (
            Truncator(strip_tags(self.content_ru)).words(10, truncate=" ...")
            if self.content_ru
            else None
        )

    def description_en(self):
        return (
            Truncator(strip_tags(self.content_en)).words(10, truncate=" ...")
            if self.content_en
            else None
        )

    class Meta:
        verbose_name = "նյութ"
        verbose_name_plural = "Նյութեր"
        ordering = ["-created_at"]
