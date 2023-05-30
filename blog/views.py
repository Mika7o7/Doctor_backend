from django.shortcuts import render
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer, ArticleMoreSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    http_method_names = ["get", "head"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ArticleMoreSerializer
        else:
            return self.serializer_class
