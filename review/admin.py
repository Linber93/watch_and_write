from django.contrib import admin
from .models import Review, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    list_display = ('title', 'producer', 'status', 'rating', 'created_on', 'review_approved')
    search_fields = ['title', 'producer']
    summernote_fields = ('opinion', 'conclusion')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(review_approved=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_filter = ('comment_approved', 'created_on')
    list_display = ('name', 'email', 'body', 'created_on', 'comment_approved')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(comment_approved=True)
