from django.contrib.auth.decorators import login_required
from django.urls import path

from .views.post import (Index, PostInfo, CategoryList, CategoryDetail,
                         like_add, like_del, PostCreate, create_comment,
                         NewsView, Favorites, PostUpdate, PostDelete, Search)
from .views.profile import ProfileDetail, follow, unfollow, FavoriteAuthors

app_name = 'blog'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('post/<int:pk>/', PostInfo.as_view(), name='post'),
    path('category/', CategoryList.as_view(), name='categories'),
    path('category/<slug>/', CategoryDetail.as_view(),
         name='category_detail'),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile'),
    path('post/<int:pk>/like/', like_add, name='like'),
    path('post/<int:pk>/dislike/', like_del, name='dislike'),

    path('profile/<int:pk>/follow/', follow, name='follow'),
    path('profile/<int:pk>/unfollow/', unfollow, name='unfollow'),

    path('follows/', login_required(FavoriteAuthors.as_view()),
         name='follows'),

    path('create_post/', login_required(PostCreate.as_view()),
         name='create_post'),
    path('news/', login_required(NewsView.as_view()), name='news'),
    path('create_comment/<int:pk>/', create_comment, name='create_comment'),
    path('likes/', login_required(Favorites.as_view()), name='likes'),
    path('post/<int:pk>/update/', login_required(PostUpdate.as_view()),
         name='update'),
    path('post/<int:pk>/delete/', login_required(PostDelete.as_view()),
         name='delete'),
    path('search/', Search.as_view(), name='search'),
]
