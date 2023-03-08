from django.contrib import admin
from .models import Review
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')
    list_display = ('title', 'producer', 'status', 'rating', 'created_on')
    search_fields = ['title', 'producer']
    summernote_fields = ('opinion', 'conclusion')
