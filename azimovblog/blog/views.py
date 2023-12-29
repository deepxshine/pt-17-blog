from django.views.generic import DetailView, ListView

from .models import Post, Category


# Create your views here.


class Index(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'


class PostInfo(DetailView):
    model = Post
    template_name = 'posts/post_info.html'
    context_object_name = 'post'


class CategoryList(ListView):  # много объектов (больше чем 1)
    model = Category
    template_name = 'posts/category_list.html'
    context_object_name = 'categories'


class CategoryDetail(DetailView):
    model = Category
    template_name = 'posts/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=context['category'])
        return context
