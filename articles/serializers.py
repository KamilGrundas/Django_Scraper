from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "source_url",
            "title",
            "published_at",
            "created_at",
            "content_text",
            "content_html",
        ]
