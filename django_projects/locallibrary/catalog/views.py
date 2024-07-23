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
    context_object_name = 'my_book_list'  # Đặt tên biến cho danh sách sách trong template
    queryset = Book.objects.filter(title__icontains='war')[:5]  # Lọc 5 sách có tiêu đề chứa 'war'
    template_name = 'books/my_arbitrary_template_name_list.html'  # Đặt tên template tùy ý

    def get_context_data(self, **kwargs):
        # Gọi thực thi cơ bản của phương thức để lấy context
        context = super().get_context_data(**kwargs)
        # Thêm dữ liệu vào context
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
