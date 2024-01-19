from django.urls import path

from .views import Index, PostInfo, CategoryList, CategoryDetail, ProfileDetail

app_name = 'blog'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('post/<int:pk>/', PostInfo.as_view(), name='post'),
    path('category/', CategoryList.as_view(), name='categories'),
    path('category/<slug>/', CategoryDetail.as_view(),
         name='category_detail'),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile')
]
