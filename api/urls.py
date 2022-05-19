from django.urls import path

from .views import ArticleView, CreateArticle, BlogView, FollowBlog, UnfollowBlog, \
    Following, ReadArticle, ArticleDetail, HistoryReadArticles

urlpatterns = [
    # Получение всех статей
    path('articles/', ArticleView.as_view()),
    # Добавление статьи
    path('articles/add/', CreateArticle.as_view()),
    # История прочитанных статей
    path('articles/history/', HistoryReadArticles.as_view()),
    # Детальный просмотр статьи
    path('articles/<int:article_id>/', ArticleDetail.as_view()),
    # Отметка статьи прочитанной
    path('articles/<int:article_id>/read/', ReadArticle.as_view()),
    # Получение персонального блога пользователя
    path('blog/<int:blog_id>/', BlogView.as_view()),
    # Подписка на персональный блог пользователя
    path('blog/<int:blog_id>/follow/', FollowBlog.as_view()),
    # Отписка от персонального блога пользователя
    path('blog/<int:blog_id>/unfollow/', UnfollowBlog.as_view()),
    # Персональная лента статей
    path('following/', Following.as_view()),
]
