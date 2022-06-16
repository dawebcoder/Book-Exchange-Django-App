from django.contrib import admin

# Register your models here.

from .models import MainMenu
from .models import Book
from .models import Post, Comment

admin.site.register(MainMenu)
admin.site.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'web', 'picture', 'price', 'username')
    search_fields = ['name', 'username']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
