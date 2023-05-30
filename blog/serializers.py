from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "id",
            "url",
            "title_hy",
            "title_ru",
            "title_en",
            "created_at",
            "image",
            "description_hy",
            "description_ru",
            "description_en",
        )



class ArticleMoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "id",
            "title_hy",
            "title_ru",
            "title_en",
            "created_at",
            "image",
            "content_hy",
            "content_ru",
            "content_en",

        )

