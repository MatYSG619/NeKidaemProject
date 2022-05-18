from django.urls import path

from .views import ArticleView, CreateArticle, BlogView, FollowBlog, UnfollowBlog, Following

urlpatterns = [
    # Получение всех статей
    path('articles/', ArticleView.as_view()),
    # Добавление статьи
    path('articles/add/', CreateArticle.as_view()),
    # Получение персонального блога пользователя
    path('blog/<int:blog_id>/', BlogView.as_view()),
    # Подписка на персональный блог пользователя
    path('blog/<int:blog_id>/follow/', FollowBlog.as_view()),
    # Отписка от персонального блога пользователя
    path('blog/<int:blog_id>/unfollow/', UnfollowBlog.as_view()),
    # Персональная лента статей
    path('following/', Following.as_view())
]
