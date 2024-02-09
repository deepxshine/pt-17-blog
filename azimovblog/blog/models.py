from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='prof')
    image = models.ImageField(upload_to='profiles', blank=True)
    birthday = models.DateField(blank=True)
    status = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    banner = models.ImageField(upload_to='banners', blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return str(self.user)


class Category(models.Model):
    label = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=2048, verbose_name="Описание")
    slug = models.SlugField(unique=True, verbose_name='Уникальное имя')
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ['label']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.label


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='post_author')
    text = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='post_category')
    pubdate = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='Likes',
                                   related_name='post_likes')
    comments = models.ManyToManyField(User, through='Comments',
                                      related_name='post_comments')

    class Meta:
        ordering = ['-pubdate']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='liked_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='com_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)

    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='flwr')  # кто подписан
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='fl_author')  # на кого
