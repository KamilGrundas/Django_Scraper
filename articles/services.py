from datetime import datetime
from urllib.parse import urlparse

from django.db import transaction

from .models import Article


def save_article(url: str, title: str, html: str, text: str, published_at: datetime) -> Article:
    domain = urlparse(url).netloc
    with transaction.atomic():
        obj, created = Article.objects.get_or_create(
            source_url=url,
            defaults=dict(
                source_domain=domain,
                title=title,
                content_html=html,
                content_text=text,
                published_at=published_at,
            ),
        )
        return obj
