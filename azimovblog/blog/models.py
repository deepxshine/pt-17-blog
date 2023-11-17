from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)

    pubdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pubdate']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты' # verbose_name+'s'

    def __str__(self):
        return self.title


class Likes(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)