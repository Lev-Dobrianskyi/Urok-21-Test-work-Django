from django import forms
from datetime import datetime
from .models import Book, BookRequest


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "genre", "year", "pages",
                  "description", "is_available"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_year(self):
        year = self.cleaned_data.get("year")
        if year and not (1000 <= year <= datetime.now().year):
            raise forms.ValidationError(
                f"Year must be between 1000 and {datetime.now().year}."
            )
        return year

    def clean_pages(self):
        pages = self.cleaned_data.get("pages")
        if pages is not None and pages <= 0:
            raise forms.ValidationError("Pages must be greater than zero.")
        return pages


class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ["reader_name", "phone"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        cleaned = (
            phone.replace(" ", "")
                 .replace("(", "")
                 .replace(")", "")
                 .replace("-", "")
        )
        digits = cleaned.lstrip("+")
        if not digits.isdigit() or not (10 <= len(digits) <= 13):
            raise forms.ValidationError(
                "Enter a valid phone number (10–13 digits, optional leading +)."
            )
        return cleaned