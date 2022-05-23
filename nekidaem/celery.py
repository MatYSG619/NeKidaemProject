from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nekidaem.settings')

app = Celery('nekidaem')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Настройка для отправки сообщения каждый день в одно и то же время
app.conf.beat_schedule = {
    'send-message-every-day': {
        'task': 'nekidaem.celery.send_articles',
        'schedule': crontab(minute='05', hour='21'),
    }
}


# tasks
@app.task
def send_articles():
    """Отправка сообщений на почту"""
    from django.core.mail import send_mail
    from accounts.models import CustomUser
    from blog.models import Article
    # Получение всех пользователей
    users = CustomUser.objects.all()
    for user in users:
        # Пять последних статей из блогов, на которые подписан пользователь
        articles = Article.objects.filter(blog__follow__in=user.follower.values('id'))[:5]
        message = 'Статьи\n'
        for article in articles:
            # Формирование сообщения
            message += f"Автор: {article.author}\n" \
                       f"Название: {article.title}\n" \
                       f"Текст: {article.text}\n"
        # Отправка сообщения
        send_mail(subject='New article',
                  message=message,
                  from_email="admin@test.ru",
                  recipient_list=[f"{user.email}"]
                  )