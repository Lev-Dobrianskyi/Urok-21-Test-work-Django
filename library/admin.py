from django.contrib import admin
from .models import Author, Genre, Book, BookRequest


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "country", "birth_year")
    search_fields = ("full_name", "country")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "year", "is_available")
    list_filter = ("genre", "author", "is_available")
    search_fields = ("title", "description")
    list_editable = ("is_available",)


@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ("reader_name", "phone", "book", "created_at")
    list_filter = ("created_at", "book")
    search_fields = ("reader_name", "phone")