from django.contrib.auth.models import AbstractUser
from blog.models import Blog


class CustomUser(AbstractUser):
    """Модель пользователя"""

    def save(self, *args, **kwargs):
        """При создании пользователя создается блог"""
        super().save(*args, **kwargs)
        Blog.objects.get_or_create(author=self, name=f'Блог {self}')
