from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm  # форма, которая будет показана
    success_url = reverse_lazy('blog:index') # страница, куда будет редирект в случае успеха
    template_name = 'user/signup.html'# шаблон
