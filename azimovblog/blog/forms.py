from django.forms import ModelForm

from .models import Post, Comments


class PostCreateForm(ModelForm): # создание формы на основе модели
    class Meta:
        model = Post # модель, на основе которой создается форма
        fields = ["title", "text", "image", "category", ]  # поля которые
        # должны быть в форме
        help_texts = {
            'title': 'Введите заголовок поста \n Не более 100 символов',
            'image': 'Загрузите картинку',
            'category': 'Выберете категорию',
        }


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comments
        fields = ["text", ]
