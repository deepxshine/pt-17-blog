from blog.forms import PostCreateForm, CommentCreateForm
from blog.models import Post, Category, Likes, Comments
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (DetailView, ListView,
                                  TemplateView, FormView, UpdateView,
                                  DeleteView)


POST_COUNT = 10


class Index(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    paginate_by = POST_COUNT


class PostInfo(DetailView):
    model = Post
    template_name = 'posts/post_info.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostInfo, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['like'] = Likes.objects.filter(
                user=self.request.user.id,
                post=context['post']
            ).exists()
        else:
            context['like'] = False

        context['like_count'] = Likes.objects.filter(
            post=context['post']
        ).count()
        context['form'] = CommentCreateForm()
        context['comments'] = Comments.objects.filter(post=context['post'])
        return context


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
        print(context['posts'])
        return context


class NewsView(ListView):
    """Метод возвращает только те посты,
     на авторов которых подписан пользователь"""
    template_name = 'posts/index.html'
    paginate_by = POST_COUNT
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.filter(
            author__fl_author__follower=self.request.user
        )
        return queryset


class Favorites(TemplateView):
    template_name = 'posts/likes.html'

    def get_context_data(self, **kwargs):
        context = super(Favorites, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            liked_post__user=self.request.user)
        return context


class PostCreate(FormView):
    template_name = 'posts/create_post.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        print(form.cleaned_data)
        Post.objects.create(author=self.request.user, **form.cleaned_data)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context


class PostUpdate(UpdateView):
    template_name = 'posts/create_post.html'
    form_class = PostCreateForm
    model = Post

    def form_valid(self, form):
        if form.instance.author == self.request.user:
            form.save()
            return redirect('blog:profile', self.request.user.id)
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
    template_name = 'posts/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'delete'
        return context

    def form_valid(self, form):
        if self.object.author == self.request.user:
            self.object.delete()
            return redirect('blog:index')
        raise PermissionDenied()


class Search(TemplateView):
    template_name = 'posts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('text')
        context['posts'] = Post.objects.filter(
            Q(title__icontains=query)
            | Q(text__icontains=query)
            | Q(author__username__icontains=query)
            | Q(author__first_name__icontains=query)
            | Q(author__last_name__icontains=query)
        )
        # sqlite не поддерживает поиск игнорируя регистр
        return context


@login_required()
def create_comment(request, pk):
    form = CommentCreateForm(request.POST or None)
    post = get_object_or_404(Post, id=pk)
    if form.is_valid():
        Comments.objects.create(post=post,
                                user=request.user, **form.cleaned_data)
    return redirect('blog:post', pk)


@login_required
def like_add(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    if not Likes.objects.filter(user=user, post=post).exists():
        Likes.objects.create(user=user, post=post)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def like_del(request, pk):
    user = request.user
    post = get_object_or_404(Post, id=pk)
    like = Likes.objects.filter(user=user, post=post)
    if like.exists():
        like.delete()
    return redirect(request.META.get('HTTP_REFERER'))
