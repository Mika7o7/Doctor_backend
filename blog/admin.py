from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    pass
