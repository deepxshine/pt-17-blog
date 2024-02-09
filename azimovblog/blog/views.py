from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .forms import PostCreateForm, CommentCreateForm
from .models import Post, Category, User, Profile, Likes, Follow, Comments


# Create your views here.


class Index(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'


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


class ProfileDetail(DetailView):
    model = User
    template_name = 'posts/profile.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.filter(
            user=context['author']).first()

        # context['posts'] = Post.objects.filter(author=context['user'])
        context['posts'] = context['author'].post_author.all()
        print(context['posts'])
        context['likes'] = Likes.objects.filter(
            post__author=context['author']).count
        if self.request.user.is_authenticated:
            context['is_follow']: bool = Follow.objects.filter(
                follower=self.request.user, author=context['author']).exists()
        context['followers_count'] = Follow.objects.filter(
            author=context['author']).count
        context['post_count'] = context['posts'].count
        return context


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


@login_required
def follow(request, pk):
    user = request.user
    profile = get_object_or_404(User, id=pk)
    if user != profile:
        if not Follow.objects.filter(follower=user, author=profile).exists():
            Follow.objects.create(follower=user, author=profile)
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow(request, pk):
    user = request.user
    profile = get_object_or_404(User, id=pk)
    if user != profile:
        follow = Follow.objects.filter(follower=user, author=profile)
        if follow.exists():
            follow.delete()
    return redirect(request.META.get('HTTP_REFERER'))


class FavoriteAuthors(TemplateView):
    template_name = 'posts/favorite_authors.html'

    def get_context_data(self, **kwargs):
        context = super(FavoriteAuthors, self).get_context_data(**kwargs)
        context['author'] = Follow.objects.filter(follower=self.request.user)
        return context


class NewsView(TemplateView):
    """Метод возвращает только те посты,
     на авторов которых подписан пользователь"""
    template_name = 'posts/news.html'

    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        authors = [obj.author for obj in Follow.objects.filter(
            follower=self.request.user)]
        print(authors)
        context['obj'] = [Post.objects.filter(
            author=author) for author in authors]
        return context


@login_required
def create_post(request):
    form = PostCreateForm()
    context = {
        'form': form
    }
    template = 'posts/create_post.html'
    return render(request, template, context)


class PostCreate(FormView):
    template_name = 'posts/create_post.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        print(form.cleaned_data)
        Post.objects.create(author=self.request.user, **form.cleaned_data)
        return redirect(self.success_url)


@login_required()
def create_comment(request, pk):
    form = CommentCreateForm(request.POST or None)
    post = get_object_or_404(Post, id=pk)
    if form.is_valid():
        Comments.objects.create(post=post,
                                user=request.user, **form.cleaned_data)
    return redirect('blog:post', pk)


class Favorites(TemplateView):
    template_name = 'posts/likes.html'

    def get_context_data(self, **kwargs):
        context = super(Favorites, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(liked_post__user=self.request.user)
        return context

