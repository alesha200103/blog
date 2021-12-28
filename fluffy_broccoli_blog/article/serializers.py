from rest_framework import serializers
from article.models import Article, Comment, Likes


class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()
    body = serializers.CharField()
    category = serializers.ChoiceField(Article.CATEGORIES)
    author_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    likes_count = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.category = validated_data.get('category', instance.category)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.likes_count = validated_data.get('likes_count', instance.likes_count)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    author_id = serializers.IntegerField()
    article_id = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class LikeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    article_id = serializers.IntegerField()
    users_id = serializers.CharField()

    def create(self, validated_data):
        return Likes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.article_id = validated_data.get('article_id', instance.article_id)
        instance.users_id = validated_data.get('users_id', instance.users_id)
        instance.save()
        return instance
