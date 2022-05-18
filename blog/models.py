from django.db import models
from django.conf import settings


class Blog(models.Model):
    """Модель для блога"""
    title = models.CharField(max_length=70, verbose_name='Заголовок', blank=False)
    text = models.TextField(max_length=140, verbose_name='Текс', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'
        ordering = ['created']

    def __str__(self):
        return self.title
