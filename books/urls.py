from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    SearchResultsListView,
    BookEditView,
    BookAddView,
    BookDeleteView,
    delete_review,
    delete_book,
)

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<uuid:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("<uuid:pk>/edit/", BookEditView.as_view(), name="book_edit"),
    path("<uuid:pk>/delete/", delete_book, name="book_delete"),
    path("new/", BookAddView.as_view(), name="book_new"),
    path("review/<int:review_pk>/delete/", delete_review, name="delete_review"),
]
