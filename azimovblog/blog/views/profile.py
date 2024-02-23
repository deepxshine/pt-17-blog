from blog.models import User, Profile, Likes, Follow
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (DetailView, TemplateView)


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


class FavoriteAuthors(TemplateView):
    template_name = 'posts/favorite_authors.html'

    def get_context_data(self, **kwargs):
        context = super(FavoriteAuthors, self).get_context_data(**kwargs)
        context['author'] = Follow.objects.filter(follower=self.request.user)
        return context


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
