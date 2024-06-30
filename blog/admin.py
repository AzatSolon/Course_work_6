from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "publish_date", "views_count")
    list_filter = ("publish_date", "title")
    verbose_name = "Статьи"
