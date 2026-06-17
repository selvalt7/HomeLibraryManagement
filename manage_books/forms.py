from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Author, Book, Category, Genre, Note, Publisher, Series, Topic

INPUT_CLASS = 'mt-2 w-full rounded border border-slate-300 bg-slate-50 p-3 text-slate-900'
SELECT_CLASS = 'mt-2 w-full rounded border border-slate-300 bg-slate-50 p-3 text-slate-900'
TEXTAREA_CLASS = 'mt-2 w-full rounded border border-slate-300 bg-slate-50 p-3 text-slate-900'
CHECKBOX_CLASS = 'rounded border-slate-300'


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'isbn', 'published_date', 'pages', 'cover', 'language',
            'publisher', 'authors', 'series', 'category', 'genres', 'topic',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'isbn': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'published_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'pages': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'cover': forms.Select(attrs={'class': SELECT_CLASS}),
            'language': forms.Select(attrs={'class': SELECT_CLASS}),
            'publisher': forms.Select(attrs={'class': SELECT_CLASS}),
            'authors': forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 6}),
            'series': forms.Select(attrs={'class': SELECT_CLASS}),
            'category': forms.Select(attrs={'class': SELECT_CLASS}),
            'genres': forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 6}),
            'topic': forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 6}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Wpisz treść notatki...'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'last_name', 'alias', 'nationality', 'title']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'alias': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'nationality': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'title': forms.Select(attrs={'class': SELECT_CLASS}),
        }


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'country', 'founded_year', 'website', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'country': forms.Select(attrs={'class': SELECT_CLASS}),
            'founded_year': forms.NumberInput(attrs={'class': INPUT_CLASS}),
            'website': forms.URLInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}),
        }


class SeriesForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name', 'description', 'authors']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
            'authors': forms.SelectMultiple(attrs={'class': SELECT_CLASS, 'size': 6}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4}),
        }
