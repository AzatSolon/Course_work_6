from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'is_published', 'views_count')
    list_filter = ('is_published', 'title')
    verbose_name = 'Статьи'
