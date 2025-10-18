from django.db import models


# Create your models here.
class Article(models.Model):
    source_url = models.URLField(unique=True)
    source_domain = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=500)
    content_html = models.TextField()
    content_text = models.TextField()
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
