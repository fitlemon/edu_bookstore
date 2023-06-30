from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.query import QuerySet
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    FormView,
)

from .models import Book, Review
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import ReviewForm
from django.urls import reverse
from django.views import View
from django.shortcuts import render

from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(0), name="dispatch")
class BookListView(LoginRequiredMixin, ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/book_list.html"
    login_url = "account_login"


class ReviewGet(DetailView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
    queryset = Book.objects.all().prefetch_related(
        "reviews__author",
    )

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        return context


class ReviewPost(SingleObjectMixin, FormView):
    model = Book
    template_name = "books/book_detail.html"
    context_object_name = "book"
    queryset = Book.objects.all().prefetch_related(
        "reviews__author",
    )
    form_class = ReviewForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.book = self.object
        review.author = self.request.user
        review.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        book = self.get_object()
        return reverse("book_detail", kwargs={"pk": book.pk}) + "#comments"


@method_decorator(cache_page(0), name="dispatch")
class BookDetailView(View):
    # login_url = "account_login"

    def get(self, request, *args, **kwargs):
        view = ReviewGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReviewPost.as_view()
        return view(request, *args, **kwargs)


class BookEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_edit.html"
    login_url = "account_login"
    permission_required = "books.special_status"
    # form_class = BookEditForm
    # def form_valid(self, form):
    #     form = BookEditForm(request.POST, request.FILES)
    #     return super().form_valid(form)
    fields = ("author", "price", "title", "cover", "file")


class SearchResultsListView(ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "books/search_results.html"

    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get("q")
        return Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )


class BookAddView(LoginRequiredMixin, CreateView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_new.html"
    login_url = "account_login"
    fields = ("author", "price", "title", "cover", "file")


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Book
    context_object_name = "book"
    template_name = "books/book_delete.html"
    permission_required = "books.special_status"
    success_url = reverse_lazy("book_list")


from django.shortcuts import get_object_or_404, redirect


def delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == "POST" and request.user == review.author:
        review.delete()

    return redirect("book_detail", pk=review.book.pk)


# FBV for delete book


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()

    return redirect("book_list")
