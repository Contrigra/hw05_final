from django.contrib import admin

# Register your models here.

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # Поля, которые должны отображаться в админке
    list_display = ("pk", "text", "pub_date", "author")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # Добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "slug")
    search_fields = ("title",)
    list_filter = ("title",)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
