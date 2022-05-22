from django.core.mail import send_mail

from accounts.models import CustomUser
from blog.models import Article


def send_articles():
    """Отправка сообщения почти автоматически"""
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
