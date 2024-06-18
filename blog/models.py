from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.CharField(max_length=100, verbose_name="Slug", null=True, blank=True)
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True, upload_to="blog/image")
    views_count = models.PositiveIntegerField(verbose_name='Просмотры', default=0)
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
