from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


@api_view(["GET"])
def get_articles(request, id=None):
    if id is not None:
        article = get_object_or_404(Article, pk=id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    articles = Article.objects.all()
    source = request.query_params.get("source")
    if source:
        articles = articles.filter(source_domain__icontains=source)

    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
