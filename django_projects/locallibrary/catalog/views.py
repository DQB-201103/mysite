from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required    
from django.views.generic import DetailView, ListView, UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, Author, BookInstance
from .forms import RenewBookForm
from .constants import PAGINATE_BY, CONTEXT_OBJECT_NAME, LOAN_STATUS
import datetime

@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'catalog/index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = PAGINATE_BY
    context_object_name = CONTEXT_OBJECT_NAME
    template_name = 'catalog/book_list.html'

    def get_queryset(self):
        first_author = Author.objects.first()
        if (first_author):
            return Book.objects.filter(author=first_author)[:5]
        else:
            return Book.objects.none()

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'

def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'
    paginate_by = PAGINATE_BY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('catalog:all-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)

class AllBorrowedView(ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    context_object_name = 'bookinstance_list'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_update_form.html'
    success_url = reverse_lazy('catalog:author-list')

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = PAGINATE_BY

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

@login_required
def my_borrowed_books(request):
    bookinstance_list = BookInstance.objects.filter(borrower=request.user).all()
    context = {
        'bookinstance_list': bookinstance_list,
        'LOAN_STATUS': LOAN_STATUS,
    }
    return render(request, 'catalog/my_borrowed_books.html', context)
