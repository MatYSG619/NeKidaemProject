from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import serializers, status

from .serializers import ArticleSerializer, BlogDetailSerializer, ArticleInBlogSerializer
from blog.models import Article, Blog, BlogFollow
from accounts.models import CustomUser


class ArticleView(APIView, LimitOffsetPagination):
    """Получение всех статей"""

    def get(self, request):
        blogs = Article.objects.all()
        result_page = self.paginate_queryset(blogs, request, view=self)
        serializer = ArticleSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class CreateArticle(APIView):
    """Добавление статьи"""

    class CreateArticleSerializer(serializers.Serializer):
        """Сериализатор для создания статьи"""
        title = serializers.CharField(max_length=70)
        text = serializers.CharField(max_length=140)

        def validate(self, data):
            """Проверка на наличие статьи"""
            request = self.context.get('request')
            title = data.get('title')
            if Article.objects.filter(author=request.user, title=title).exists():
                raise serializers.ValidationError(detail="Пост с таким заголовком уже существует",
                                                  code=status.HTTP_400_BAD_REQUEST
                                                  )
            return data

    def post(self, request):
        article = request.data.get('article')
        serializer = self.CreateArticleSerializer(data=article, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            Article.objects.create(blog_id=request.user.pk, author=request.user, **serializer.validated_data)
        return Response({"success": "Article created successfully"})


class BlogView(APIView):
    """Получение персонального блога"""

    def get(self, request, blog_id):
        blog = Blog.objects.filter(pk=blog_id)
        serializer = BlogDetailSerializer(blog, many=True)
        article = Article.objects.filter(author=blog_id)
        article_serializer = ArticleInBlogSerializer(article, many=True)
        return Response({'blog': serializer.data, 'articles': article_serializer.data})


class FollowBlog(APIView):
    """Подписка на блог"""

    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        if blog.author == request.user:
            return Response({"error": "Вы не можете подписаться сами на себя!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            BlogFollow.objects.get(blog=blog, user=request.user)
            return Response({"message": "Вы уже подписаны на данного пользователя"}, status=status.HTTP_423_LOCKED)
        except ObjectDoesNotExist:
            BlogFollow.objects.create(blog=blog, user=request.user)
            return Response({"success": "Вы успешно подписались на данного пользователя"},
                            status=status.HTTP_201_CREATED)


class UnfollowBlog(APIView):
    """Отписка от блога"""

    def get(self, request, blog_id):
        blog = get_object_or_404(Blog, pk=blog_id)
        if blog.author == request.user:
            return Response({"error": "Вы не можете отписаться от самого себя"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj = BlogFollow.objects.get(blog=blog, user=request.user)
            obj.delete()
            return Response({"success": "Вы успешно отписались от этого пользователя"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Вы не подписаны на данного пользователя"}, status=status.HTTP_400_BAD_REQUEST)


class Following(APIView, LimitOffsetPagination):
    """Персональная лента с пагинацией 10 постов"""

    def get(self, request):
        user = request.user
        # user.follower.values('id') - id блогов, на которые подписан пользователь
        # Лента статей не более 500
        blog_obj = Article.objects.filter(blog__follow__in=user.follower.values('id'))[:500]
        result_page = self.paginate_queryset(blog_obj, request, view=self)
        serializer = ArticleSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class ArticleDetail(APIView):
    """Детальный просмотр статьи"""

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response({"article": serializer.data})


class ReadArticle(APIView):
    """Отметка статьи прочитанной"""

    def get(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, id=article_id)
        user.read.add(article)
        return Response({'success': "Статья успешно прочитана"}, status=status.HTTP_200_OK)


class HistoryReadArticles(APIView):
    """История прочитанных статей"""

    def get(self, request):
        user = request.user
        try:
            articles = Article.objects.filter(id__in=user.read.values('id'))
            serializer = ArticleSerializer(articles, many=True)
            return Response({"articles": serializer.data})
        except ObjectDoesNotExist:
            return Response({"message": "У вас еще нет прочитанных статей"})


def send_articles(request):
    """Отправка сообщения на почту пользователям в ручную через панель администрирования"""
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
    return redirect(request.META.get('HTTP_REFERER'))
