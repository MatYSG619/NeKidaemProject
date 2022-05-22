from django.contrib import admin
from .models import Article, BlogFollow


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'author']
    ordering = ['created']
    change_list_template = 'admin/change_list.html'


@admin.register(BlogFollow)
class BlogFollow(admin.ModelAdmin):
    list_display = ['blog', 'user']
    ordering = ['blog']
