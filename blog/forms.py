from django.forms import ModelForm
from mail.forms import StyleMixin
from blog.models import Blog


class PostForm(StyleMixin, ModelForm):
    """
    Форма создания статьи
    """

    class Meta:
        model = Blog
        exclude = ("is_published", "views_count")
