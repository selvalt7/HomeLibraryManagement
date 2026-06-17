from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AuthorForm, BookForm, CategoryForm, GenreForm, NoteForm,
    PublisherForm, SeriesForm, SignupForm, TopicForm,
)
from .models import Author, Book, Category, Genre, Note, Publisher, Series, Topic


def _save_book(form):
    book = form.save(commit=False)
    book.save()
    form.save_m2m()
    authors = list(book.authors.all())
    if authors:
        book.author = ', '.join(f'{a.name} {a.last_name}' for a in authors)
    elif not book.author:
        book.author = 'Nieznany'
    book.save(update_fields=['author'])
    return book


def index(request):
    genres = Genre.objects.all()
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    series = Series.objects.all()
    notes = Note.objects.all()
    books = Book.objects.all().select_related('publisher', 'series', 'category').prefetch_related('authors', 'genres', 'topic')
    topics = Topic.objects.all()
    categories = Category.objects.all()

    genre_id = request.GET.get('genre')
    genre_name = None
    if genre_id:
        books = books.filter(genres__id=genre_id)
        genre_name = Genre.objects.filter(id=genre_id).values_list('name', flat=True).first()

    topic_id = request.GET.get('topic')
    topic_name = None
    if topic_id:
        books = books.filter(topic__id=topic_id)
        topic_name = Topic.objects.filter(id=topic_id).values_list('name', flat=True).first()

    category_id = request.GET.get('category')
    category_name = None
    if category_id:
        books = books.filter(category__id=category_id)
        category_name = Category.objects.filter(id=category_id).values_list('name', flat=True).first()

    author_id = request.GET.get('author')
    author_name = None
    if author_id:
        books = books.filter(authors__id=author_id)
        author_obj = Author.objects.filter(id=author_id).first()
        if author_obj:
            author_name = f'{author_obj.name} {author_obj.last_name}'

    publisher_id = request.GET.get('publisher')
    publisher_name = None
    if publisher_id:
        books = books.filter(publisher__id=publisher_id)
        publisher_name = Publisher.objects.filter(id=publisher_id).values_list('name', flat=True).first()

    series_id = request.GET.get('series')
    series_name = None
    if series_id:
        books = books.filter(series__id=series_id)
        series_name = Series.objects.filter(id=series_id).values_list('name', flat=True).first()

    is_read = request.GET.get('is_read')
    if is_read == 'true':
        books = books.filter(is_read=True)
    elif is_read == 'false':
        books = books.filter(is_read=False)

    is_favorite = request.GET.get('is_favorite')
    if is_favorite == 'true':
        books = books.filter(is_favorite=True)

    books = books.distinct()

    return render(request, 'manage_books/index.html.jinja', {
        'genres': genres,
        'authors': authors,
        'publishers': publishers,
        'series': series,
        'notes': notes,
        'books': books,
        'topics': topics,
        'categories': categories,
        'favorite_books': books.filter(is_favorite=True),
        'read_books': books.filter(is_read=True),
        'genre_id': genre_id,
        'genre_name': genre_name,
        'topic_id': topic_id,
        'topic_name': topic_name,
        'category_id': category_id,
        'category_name': category_name,
        'author_id': author_id,
        'author_name': author_name,
        'publisher_id': publisher_id,
        'publisher_name': publisher_name,
        'series_id': series_id,
        'series_name': series_name,
        'is_read': is_read,
        'is_favorite': is_favorite,
    })


def book(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    notes = Note.objects.filter(book=book_obj).order_by('-created_at')
    return render(request, 'manage_books/book.html.jinja', {'book': book_obj, 'notes': notes})


def author(request, author_id):
    author_obj = get_object_or_404(Author, id=author_id)
    books = author_obj.books.all().order_by('title')
    return render(request, 'manage_books/author.html.jinja', {'author': author_obj, 'books': books})


def publisher(request, publisher_id):
    publisher_obj = get_object_or_404(Publisher, id=publisher_id)
    books = Book.objects.filter(publisher=publisher_obj).order_by('title')
    return render(request, 'manage_books/publisher.html.jinja', {'publisher': publisher_obj, 'books': books})


def series(request, series_id):
    series_obj = get_object_or_404(Series, id=series_id)
    books = Book.objects.filter(series=series_obj).order_by('published_date')
    return render(request, 'manage_books/series.html.jinja', {'series': series_obj, 'books': books})


def note(request, note_id):
    note_obj = get_object_or_404(Note, id=note_id)
    return render(request, 'manage_books/note.html.jinja', {'note': note_obj})


def authors_list(request):
    authors = Author.objects.all().order_by('name', 'last_name')
    return render(request, 'manage_books/authors_list.html.jinja', {'authors': authors})


def publishers_list(request):
    publishers = Publisher.objects.all().order_by('name')
    return render(request, 'manage_books/publishers_list.html.jinja', {'publishers': publishers})


def series_list(request):
    series_objs = Series.objects.all().order_by('name')
    return render(request, 'manage_books/series_list.html.jinja', {'series': series_objs})


def genres_list(request):
    genres = Genre.objects.all().order_by('name')
    return render(request, 'manage_books/genres_list.html.jinja', {'genres': genres})


def topics_list(request):
    topics = Topic.objects.all().order_by('name')
    return render(request, 'manage_books/topics_list.html.jinja', {'topics': topics})


def categories_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'manage_books/categories_list.html.jinja', {'categories': categories})


def notes_list(request):
    notes = Note.objects.all().order_by('-created_at')
    return render(request, 'manage_books/notes_list.html.jinja', {'notes': notes})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Zalogowano pomyślnie.')
        return redirect(request.GET.get('next') or 'index')
    return render(request, 'manage_books/login.html.jinja', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Wylogowano pomyślnie.')
    return redirect('index')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Konto zostało utworzone. Witaj w bibliotece!')
        return redirect('index')
    return render(request, 'manage_books/signup.html.jinja', {'form': form})


@login_required
def book_add(request):
    form = BookForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        book_obj = _save_book(form)
        messages.success(request, 'Książka została dodana.')
        return redirect('book', book_id=book_obj.id)
    return render(request, 'manage_books/book_form.html.jinja', {
        'form': form,
        'title': 'Dodaj nową książkę',
        'submit_label': 'Zapisz książkę',
    })


@login_required
def book_edit(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    form = BookForm(request.POST or None, instance=book_obj)
    if request.method == 'POST' and form.is_valid():
        _save_book(form)
        messages.success(request, 'Książka została zaktualizowana.')
        return redirect('book', book_id=book_obj.id)
    return render(request, 'manage_books/book_form.html.jinja', {
        'form': form,
        'book': book_obj,
        'title': 'Edytuj książkę',
        'submit_label': 'Zapisz zmiany',
    })


@login_required
def book_delete(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        title = book_obj.title
        book_obj.delete()
        messages.success(request, f'Książka „{title}” została usunięta.')
        return redirect('index')
    return render(request, 'manage_books/book_delete_confirm.html.jinja', {'book': book_obj})


@login_required
def mark_read(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    book_obj.is_read = True
    book_obj.save(update_fields=['is_read'])
    messages.success(request, 'Książka oznaczona jako przeczytana.')
    return redirect('book', book_id=book_obj.id)


@login_required
def mark_unread(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    book_obj.is_read = False
    book_obj.save(update_fields=['is_read'])
    messages.success(request, 'Książka oznaczona jako nieprzeczytana.')
    return redirect('book', book_id=book_obj.id)


@login_required
def favorite_add(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    book_obj.is_favorite = True
    book_obj.save(update_fields=['is_favorite'])
    messages.success(request, 'Książka dodana do ulubionych.')
    return redirect('book', book_id=book_obj.id)


@login_required
def favorite_remove(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    book_obj.is_favorite = False
    book_obj.save(update_fields=['is_favorite'])
    messages.success(request, 'Książka usunięta z ulubionych.')
    return redirect('book', book_id=book_obj.id)


@login_required
def add_note(request, book_id):
    book_obj = get_object_or_404(Book, id=book_id)
    if request.method != 'POST':
        return redirect('book', book_id=book_obj.id)
    form = NoteForm(request.POST)
    if form.is_valid():
        note_obj = form.save(commit=False)
        note_obj.book = book_obj
        note_obj.save()
        messages.success(request, 'Notatka została zapisana.')
    else:
        messages.error(request, 'Nie udało się zapisać notatki. Uzupełnij treść.')
    return redirect('book', book_id=book_obj.id)


@login_required
def note_edit(request, note_id):
    note_obj = get_object_or_404(Note, id=note_id)
    form = NoteForm(request.POST or None, instance=note_obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Notatka została zaktualizowana.')
        return redirect('book', book_id=note_obj.book_id)
    return render(request, 'manage_books/note_form.html.jinja', {
        'form': form,
        'note': note_obj,
        'title': 'Edytuj notatkę',
        'submit_label': 'Zapisz zmiany',
    })


def _dictionary_form_view(request, form_class, template_name, success_message, redirect_name, instance=None, extra_context=None):
    form = form_class(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        messages.success(request, success_message)
        if redirect_name == 'author':
            return redirect('author', author_id=obj.id)
        if redirect_name == 'publisher':
            return redirect('publisher', publisher_id=obj.id)
        if redirect_name == 'series':
            return redirect('series', series_id=obj.id)
        if redirect_name == 'genres_list':
            return redirect('genres_list')
        if redirect_name == 'topics_list':
            return redirect('topics_list')
        if redirect_name == 'categories_list':
            return redirect('categories_list')
        return redirect(redirect_name)
    context = {'form': form}
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context)


@login_required
def author_add(request):
    return _dictionary_form_view(
        request, AuthorForm, 'manage_books/author_form.html.jinja',
        'Autor został dodany.', 'authors_list',
        extra_context={'title': 'Dodaj autora', 'submit_label': 'Zapisz autora'},
    )


@login_required
def author_edit(request, author_id):
    author_obj = get_object_or_404(Author, id=author_id)
    return _dictionary_form_view(
        request, AuthorForm, 'manage_books/author_form.html.jinja',
        'Autor został zaktualizowany.', 'author', author_obj,
        extra_context={'title': 'Edytuj autora', 'submit_label': 'Zapisz zmiany', 'author': author_obj},
    )


@login_required
def author_delete(request, author_id):
    author_obj = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        try:
            name = str(author_obj)
            author_obj.delete()
            messages.success(request, f'Autor „{name}” został usunięty.')
            return redirect('authors_list')
        except ProtectedError:
            messages.error(request, 'Nie można usunąć autora powiązanego z książkami lub seriami.')
            return redirect('author', author_id=author_obj.id)
    return render(request, 'manage_books/delete_confirm.html.jinja', {
        'object': author_obj,
        'object_label': 'autora',
        'cancel_url': f'/author/{author_obj.id}/',
        'post_url': f'/author/{author_obj.id}/delete/',
    })


@login_required
def publisher_add(request):
    return _dictionary_form_view(
        request, PublisherForm, 'manage_books/publisher_form.html.jinja',
        'Wydawca został dodany.', 'publishers_list',
        extra_context={'title': 'Dodaj wydawcę', 'submit_label': 'Zapisz wydawcę'},
    )


@login_required
def publisher_edit(request, publisher_id):
    publisher_obj = get_object_or_404(Publisher, id=publisher_id)
    return _dictionary_form_view(
        request, PublisherForm, 'manage_books/publisher_form.html.jinja',
        'Wydawca został zaktualizowany.', 'publisher', publisher_obj,
        extra_context={'title': 'Edytuj wydawcę', 'submit_label': 'Zapisz zmiany', 'publisher': publisher_obj},
    )


@login_required
def publisher_delete(request, publisher_id):
    publisher_obj = get_object_or_404(Publisher, id=publisher_id)
    if request.method == 'POST':
        try:
            name = publisher_obj.name
            publisher_obj.delete()
            messages.success(request, f'Wydawca „{name}” został usunięty.')
            return redirect('publishers_list')
        except ProtectedError:
            messages.error(request, 'Nie można usunąć wydawcy powiązanego z książkami.')
            return redirect('publisher', publisher_id=publisher_obj.id)
    return render(request, 'manage_books/delete_confirm.html.jinja', {
        'object': publisher_obj,
        'object_label': 'wydawcę',
        'cancel_url': f'/publisher/{publisher_obj.id}/',
        'post_url': f'/publisher/{publisher_obj.id}/delete/',
    })


@login_required
def series_add(request):
    return _dictionary_form_view(
        request, SeriesForm, 'manage_books/series_form.html.jinja',
        'Seria została dodana.', 'series_list',
        extra_context={'title': 'Dodaj serię', 'submit_label': 'Zapisz serię'},
    )


@login_required
def series_edit(request, series_id):
    series_obj = get_object_or_404(Series, id=series_id)
    return _dictionary_form_view(
        request, SeriesForm, 'manage_books/series_form.html.jinja',
        'Seria została zaktualizowana.', 'series', series_obj,
        extra_context={'title': 'Edytuj serię', 'submit_label': 'Zapisz zmiany', 'series': series_obj},
    )


@login_required
def series_delete(request, series_id):
    series_obj = get_object_or_404(Series, id=series_id)
    if request.method == 'POST':
        try:
            name = series_obj.name
            series_obj.delete()
            messages.success(request, f'Seria „{name}” została usunięta.')
            return redirect('series_list')
        except ProtectedError:
            messages.error(request, 'Nie można usunąć serii powiązanej z książkami.')
            return redirect('series', series_id=series_obj.id)
    return render(request, 'manage_books/delete_confirm.html.jinja', {
        'object': series_obj,
        'object_label': 'serię',
        'cancel_url': f'/series/{series_obj.id}/',
        'post_url': f'/series/{series_obj.id}/delete/',
    })


@login_required
def genre_add(request):
    return _dictionary_form_view(
        request, GenreForm, 'manage_books/genre_form.html.jinja',
        'Gatunek został dodany.', 'genres_list',
        extra_context={'title': 'Dodaj gatunek', 'submit_label': 'Zapisz gatunek'},
    )


@login_required
def genre_edit(request, genre_id):
    genre_obj = get_object_or_404(Genre, id=genre_id)
    return _dictionary_form_view(
        request, GenreForm, 'manage_books/genre_form.html.jinja',
        'Gatunek został zaktualizowany.', 'genres_list', genre_obj,
        extra_context={'title': 'Edytuj gatunek', 'submit_label': 'Zapisz zmiany', 'genre': genre_obj},
    )


@login_required
def genre_delete(request, genre_id):
    genre_obj = get_object_or_404(Genre, id=genre_id)
    if request.method == 'POST':
        name = genre_obj.name
        genre_obj.delete()
        messages.success(request, f'Gatunek „{name}” został usunięty.')
        return redirect('genres_list')
    return render(request, 'manage_books/delete_confirm.html.jinja', {
        'object': genre_obj,
        'object_label': 'gatunek',
        'cancel_url': '/genres/',
        'post_url': f'/genre/{genre_obj.id}/delete/',
    })


@login_required
def topic_add(request):
    return _dictionary_form_view(
        request, TopicForm, 'manage_books/topic_form.html.jinja',
        'Temat został dodany.', 'topics_list',
        extra_context={'title': 'Dodaj temat', 'submit_label': 'Zapisz temat'},
    )


@login_required
def topic_edit(request, topic_id):
    topic_obj = get_object_or_404(Topic, id=topic_id)
    return _dictionary_form_view(
        request, TopicForm, 'manage_books/topic_form.html.jinja',
        'Temat został zaktualizowany.', 'topics_list', topic_obj,
        extra_context={'title': 'Edytuj temat', 'submit_label': 'Zapisz zmiany', 'topic': topic_obj},
    )


@login_required
def topic_delete(request, topic_id):
    topic_obj = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        name = topic_obj.name
        topic_obj.delete()
        messages.success(request, f'Temat „{name}” został usunięty.')
        return redirect('topics_list')
    return render(request, 'manage_books/delete_confirm.html.jinja', {
        'object': topic_obj,
        'object_label': 'temat',
        'cancel_url': '/topics/',
        'post_url': f'/topic/{topic_obj.id}/delete/',
    })


@login_required
def category_add(request):
    return _dictionary_form_view(
        request, CategoryForm, 'manage_books/category_form.html.jinja',
        'Dział został dodany.', 'categories_list',
        extra_context={'title': 'Dodaj dział', 'submit_label': 'Zapisz dział'},
    )


@login_required
def category_edit(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    return _dictionary_form_view(
        request, CategoryForm, 'manage_books/category_form.html.jinja',
        'Dział został zaktualizowany.', 'categories_list', category_obj,
        extra_context={'title': 'Edytuj dział', 'submit_label': 'Zapisz zmiany', 'category': category_obj},
    )


@login_required
def category_delete(request, category_id):
    category_obj = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = category_obj.name
        category_obj.delete()
        messages.success(request, f'Dział „{name}” został usunięty.')
        return redirect('categories_list')
    return render(request, 'manage_books/delete_confirm.html.jinja', {
        'object': category_obj,
        'object_label': 'dział',
        'cancel_url': '/categories/',
        'post_url': f'/category/{category_obj.id}/delete/',
    })
