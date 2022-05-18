from django.db import models
from django.conf import settings


class Blog(models.Model):
    """Модель для блога"""
    name = models.CharField(max_length=50, verbose_name='Название блога')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'

    def __str__(self):
        return self.name


class Article(models.Model):
    """Модель для статей"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_articles', verbose_name='Блог')
    title = models.CharField(max_length=70, verbose_name='Заголовок', blank=False)
    text = models.TextField(max_length=140, verbose_name='Текс', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['created']

    def __str__(self):
        return self.title


class BlogFollow(models.Model):
    """Модель для подписки"""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='follow', verbose_name='Блог')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик'
                             )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
