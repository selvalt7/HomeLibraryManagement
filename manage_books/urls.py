from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('book/add/', views.book_add, name='book_add'),
    path('book/<int:book_id>/', views.book, name='book'),
    path('book/<int:book_id>/edit/', views.book_edit, name='book_edit'),
    path('book/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('book/<int:book_id>/mark-read/', views.mark_read, name='mark_read'),
    path('book/<int:book_id>/mark-unread/', views.mark_unread, name='mark_unread'),
    path('book/<int:book_id>/favorite/add/', views.favorite_add, name='favorite_add'),
    path('book/<int:book_id>/favorite/remove/', views.favorite_remove, name='favorite_remove'),
    path('book/<int:book_id>/notes/add/', views.add_note, name='add_note'),

    path('authors/', views.authors_list, name='authors_list'),
    path('author/add/', views.author_add, name='author_add'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('author/<int:author_id>/edit/', views.author_edit, name='author_edit'),
    path('author/<int:author_id>/delete/', views.author_delete, name='author_delete'),

    path('publishers/', views.publishers_list, name='publishers_list'),
    path('publisher/add/', views.publisher_add, name='publisher_add'),
    path('publisher/<int:publisher_id>/', views.publisher, name='publisher'),
    path('publisher/<int:publisher_id>/edit/', views.publisher_edit, name='publisher_edit'),
    path('publisher/<int:publisher_id>/delete/', views.publisher_delete, name='publisher_delete'),

    path('series/', views.series_list, name='series_list'),
    path('series/add/', views.series_add, name='series_add'),
    path('series/<int:series_id>/', views.series, name='series'),
    path('series/<int:series_id>/edit/', views.series_edit, name='series_edit'),
    path('series/<int:series_id>/delete/', views.series_delete, name='series_delete'),

    path('genres/', views.genres_list, name='genres_list'),
    path('genre/add/', views.genre_add, name='genre_add'),
    path('genre/<int:genre_id>/edit/', views.genre_edit, name='genre_edit'),
    path('genre/<int:genre_id>/delete/', views.genre_delete, name='genre_delete'),

    path('topics/', views.topics_list, name='topics_list'),
    path('topic/add/', views.topic_add, name='topic_add'),
    path('topic/<int:topic_id>/edit/', views.topic_edit, name='topic_edit'),
    path('topic/<int:topic_id>/delete/', views.topic_delete, name='topic_delete'),

    path('categories/', views.categories_list, name='categories_list'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('category/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    path('note/<int:note_id>/', views.note, name='note'),
    path('note/<int:note_id>/edit/', views.note_edit, name='note_edit'),
    path('notes/', views.notes_list, name='notes_list'),
]
