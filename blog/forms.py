from django.forms import ModelForm
from mail.forms import StyleMixin
from blog.models import Blog


class BlogForm(StyleMixin, ModelForm):
    """
    Форма создания статьи
    """

    class Meta:
        model = Blog
        exclude = ['slug', 'views_count']
