from django.contrib import admin
from .models import Post, User, Comment

admin.site.register(User)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}