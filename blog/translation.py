from modeltranslation.translator import TranslationOptions, register

from .models import Article, Category


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ("title", "content")
