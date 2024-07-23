from django.shortcuts import render, get_object_or_404
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from django.views.generic import DetailView

PAGINATE_BY = 10
CONTEXT_OBJECT_NAME = 'my_book_list'

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = PAGINATE_BY
    context_object_name = CONTEXT_OBJECT_NAME
    template_name = 'books/my_arbitrary_template_name_list.html'

    def get_queryset(self):
        first_author = Author.objects.first()
        if first_author:
            return Book.objects.filter(author=first_author)[:5]
        else:
            return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

