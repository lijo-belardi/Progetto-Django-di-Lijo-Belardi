from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "datetime", "user"]
    list_filter = ["user", "datetime"]
    search_fields = ["title", "content"]
    ordering = ["datetime"]

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
