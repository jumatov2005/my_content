from django.contrib import admin
from .models import MediaContent, Comment


@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'is_active', 'publish_time', 'created_at')
    list_filter = ('is_active', 'content_type', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-publish_time',)
    list_editable = ('is_active', 'publish_time')  # Tez o‘zgartirish uchun

    # Admin form ko‘rinishi
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'description', 'content_type', 'file')
        }),
        ('Holat', {
            'fields': ('is_active', 'publish_time')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'text', 'content__title')

