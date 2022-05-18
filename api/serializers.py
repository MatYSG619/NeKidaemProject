from django.conf import settings

from rest_framework import serializers

from blog.models import Article, Blog
from accounts.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей"""

    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для статьи"""
    author = CustomUserSerializer()

    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'created', 'author']


class ArticleInBlogSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра статей в блоге"""
    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'created']


class BlogDetailSerializer(serializers.ModelSerializer):
    """Детальный просмотр блога пользователя"""
    author = CustomUserSerializer()

    class Meta:
        model = Blog
        fields = ['id', 'name', 'author']
