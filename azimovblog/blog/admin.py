from django.contrib import admin

# Register your models here.
from .models import Post, Comments, Likes, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug', 'get_post_count')
    search_fields = ('label', 'slug')

    def get_post_count(self, obj):
        return obj.post_category.count()

    get_post_count.short_description = 'Количество постов'


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    pass


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    pass
