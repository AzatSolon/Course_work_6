from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=150, null=True, verbose_name="Заголовок"
                    ),
                ),
                (
                    "body",
                    models.TextField(blank=True, null=True, verbose_name="Содержимое"),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "views_count",
                    models.IntegerField(
                        default=0, verbose_name="Количество просмотров"
                    ),
                ),
                (
                    "publish_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(default=True, verbose_name="Опубликован"),
                ),
            ],
            options={
                "verbose_name": "Запись",
                "verbose_name_plural": "Записи",
            },
        ),
    ]
