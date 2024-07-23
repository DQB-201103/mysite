from django.shortcuts import render, get_object_or_404
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from django.views.generic import DetailView

def index(request):
    """Hàm view cho trang chính của trang web."""
    # Tạo số lượng của một số đối tượng chính
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Đếm số lần truy cập
    num_visits = request.session.get('num_visits', 0)  
    request.session['num_visits'] = num_visits + 1  

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,  # Truyền số lần truy cập vào context
    }

    # Render template HTML index.html với dữ liệu trong biến context
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'  
    queryset = Book.objects.all()  
    template_name = 'books/book_list.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'

    def book_detail_view(request, primary_key):
        """Hàm view cho chi tiết sách."""
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'catalog/book_detail.html', context={'book': book})
    
class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

from django.views.generic import ListView
from .models import Author

class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'
    paginate_by = 10
    queryset = Author.objects.all()  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

from django.contrib.auth.decorators import login_required, permission_required    
from .models import BookInstance
from .forms import RenewBookForm
import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic import ListView

class AllBorrowedView(ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    context_object_name = 'bookinstance_list'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'catalog/author_update_form.html'
    success_url = reverse_lazy('author-list')