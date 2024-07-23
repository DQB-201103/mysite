# catalog/urls.py

from django.urls import path
from . import views
from .views import (
    index,
    renew_book_librarian,
    my_borrowed,
    BookListView, 
    BookDetailView, 
    AuthorListView, 
    AuthorDetailView, 
    AllBorrowedView, 
    AuthorUpdate, 
    LoanedBooksByUserListView,
)

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('all-borrowed/', views.AllBorrowedView.as_view(), name='all-borrowed'),
    path('author/<int:pk>/update/', AuthorUpdate.as_view(), name='author-update'),
    path('mybooks/', LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('my-borrowed/', views.my_borrowed, name='my-borrowed'),
]
