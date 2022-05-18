from django.contrib import admin
from .models import Article, BlogFollow


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'author']
    ordering = ['created']


@admin.register(BlogFollow)
class BlogFollow(admin.ModelAdmin):
    list_display = ['blog', 'user']
    ordering = ['blog']
