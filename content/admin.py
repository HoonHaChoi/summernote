from django.contrib import admin
from .models import Post, Apply ,Chatroom
from .forms import PostForm

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin

class Message(admin.TabularInline):

    model =  Chatroom


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    form = PostForm
    summernote_fields = ('content',)
    list_display = ['title', 'content', 'user_count', 'user_max_count', 'deadline','author']
    inlines = [Message]


@admin.register(Apply)
class ApplyAdmin(admin.ModelAdmin):
    list_display = ['id' , 'user', 'post']
    list_display_links = ['id']

