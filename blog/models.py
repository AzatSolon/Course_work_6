from django.db import models

from mail.models import NULLABLE


class Blog(models.Model):
    """
     Модель блога
    """
    title = models.CharField(max_length=150, verbose_name="Заголовок", **NULLABLE)
    body = models.TextField(verbose_name="Содержимое", **NULLABLE)
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    image = models.ImageField(upload_to="blog/", verbose_name="Изображение", **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")
    publish_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.title}: {self.views_count}, {self.publish_date}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
