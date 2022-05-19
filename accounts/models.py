from django.db import models
from django.contrib.auth.models import AbstractUser

from blog.models import Blog, Article


class CustomUser(AbstractUser):
    """Модель пользователя"""
    # Отметка статьи прочитанной
    read = models.ManyToManyField(Article, related_name='readers', verbose_name='Прочитано', blank=True, default=None)

    def save(self, *args, **kwargs):
        """При создании пользователя создается блог"""
        super().save(*args, **kwargs)
        Blog.objects.get_or_create(author=self, name=f'Блог {self}')
