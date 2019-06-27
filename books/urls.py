from django.urls import path
from .views import ListBooksView, BooksDetailView, external_books


urlpatterns = [
    path('books/', ListBooksView.as_view(), name="books-all"),
    path('books/<int:pk>/', BooksDetailView.as_view(), name="book-detail"),
    path('external-books/', external_books, name="external-books"),



]	