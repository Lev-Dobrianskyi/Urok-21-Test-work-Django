from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Book, Author, Genre, BookRequest
from .forms import BookForm, BookRequestForm
from .decorators import staff_required


def home(request):
    newest = Book.objects.select_related("author", "genre")[:3]
    return render(request, "library/home.html", {"newest": newest})


def book_list(request):
    books = Book.objects.select_related("author", "genre")
    q = request.GET.get("q", "").strip()
    genre_id = request.GET.get("genre", "").strip()

    if q:
        books = books.filter(
            Q(title__icontains=q) | Q(author__full_name__icontains=q)
        )
    if genre_id.isdigit():
        books = books.filter(genre_id=genre_id)

    return render(
        request,
        "library/book_list.html",
        {
            "books": books,
            "genres": Genre.objects.all(),
            "active_genre": genre_id,
            "q": q,
        },
    )


def book_detail(request, pk):
    book = get_object_or_404(
        Book.objects.select_related("author", "genre"), pk=pk
    )
    return render(request, "library/book_detail.html", {"book": book})


def author_list(request):
    authors = Author.objects.all()
    return render(request, "library/author_list.html", {"authors": authors})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.select_related("genre")
    return render(
        request,
        "library/author_detail.html",
        {"author": author, "books": books},
    )


@staff_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, "Book was created successfully.")
            return redirect("library:book_detail", pk=book.pk)
    else:
        form = BookForm()
    return render(
        request,
        "library/book_form.html",
        {"form": form, "title": "New book"},
    )


@staff_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book was updated successfully.")
            return redirect("library:book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(
        request,
        "library/book_form.html",
        {"form": form, "title": f"Edit: {book.title}"},
    )


@staff_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book was deleted successfully.")
        return redirect("library:book_list")
    return render(request, "library/book_confirm.html", {"book": book})


def request_create(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if not book.is_available:
        messages.error(request, "This book is currently checked out and unavailable.")
        return redirect("library:book_detail", pk=book.pk)

    if request.method == "POST":
        form = BookRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.book = book
            req.save()
            messages.success(request, "Request submitted successfully.")
            return redirect("library:book_detail", pk=book.pk)
    else:
        form = BookRequestForm()
    return render(
        request,
        "library/request_form.html",
        {"form": form, "book": book},
    )


@staff_required
def request_list(request):
    requests = BookRequest.objects.select_related("book")
    return render(request, "library/request_list.html", {"requests": requests})