from django.db import models
from django.conf import settings


class Article(models.Model):
    CATEGORIES = [
        ("cinema", "cinema"),
        ("travelling", "travelling"),
        ("science", "science"),
        ("technology", "technology"),
        ("style", "style"),
        ("celebrities", "celebrities"),
        ("culture", "culture"),
        ("sport", "sport"),
        ("finance", "finance"),
        ("politics", "politics")
    ]

    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    category = models.CharField(max_length=11, default="cinema")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey("Article", related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Likes(models.Model):
    article = models.OneToOneField("Article", related_name='likes', on_delete=models.CASCADE)
    users_id = models.TextField(default="")
