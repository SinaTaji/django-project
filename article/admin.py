from django.contrib import admin
from .models import ArticleCategory, Article,ArticleComment
from django.http import HttpRequest


class AdminCategory(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_active']
    list_editable = ['is_active', 'category']


class AdminComment(admin.ModelAdmin):
    list_display = ['article', 'user', 'text']


class AdminArticle(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']

    def save_model(self, request: HttpRequest, obj: Article, form, change):
        if not change:
            obj.auther = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(ArticleCategory, AdminCategory)
admin.site.register(Article, AdminArticle)
admin.site.register(ArticleComment, AdminComment)
