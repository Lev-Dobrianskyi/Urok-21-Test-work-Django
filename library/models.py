from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime


class Author(models.Model):
    full_name = models.CharField("Full name", max_length=150, default="")
    country = models.CharField("Country", max_length=80, default="")
    birth_year = models.IntegerField("Birth year", null=True, blank=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.CharField("Name", max_length=100)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField("Title", max_length=150, default="")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books", verbose_name="Author", null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="books", verbose_name="Genre", null=True)
    year = models.IntegerField("Year", null=True)
    pages = models.IntegerField("Pages", null=True)
    description = models.TextField("Description", blank=True)
    is_available = models.BooleanField("Available", default=True)
    created_at = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.year and not (1000 <= self.year <= datetime.now().year):
            raise ValidationError(
                {"year": f"Year must be between 1000 and {datetime.now().year}."}
            )
        if self.pages is not None and self.pages <= 0:
            raise ValidationError({"pages": "Pages must be greater than zero."})


class BookRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="requests", verbose_name="Book")
    reader_name = models.CharField("Reader name", max_length=100, default="")
    phone = models.CharField("Phone", max_length=20)
    created_at = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Request from {self.reader_name} for '{self.book.title}'"