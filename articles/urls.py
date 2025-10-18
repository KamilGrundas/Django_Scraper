from django.urls import path

from articles.views import get_articles

urlpatterns = [
    path("articles/", get_articles),
    path("articles/<int:id>/", get_articles),
]
