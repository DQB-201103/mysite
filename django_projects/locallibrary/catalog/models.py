from django.db import models

# Create your models here.
class Genre(models.Model):
    """Model đại diện cho thể loại sách."""
    name = models.CharField(max_length=200, help_text='Nhập thể loại sách (ví dụ: Khoa học viễn tưởng)')

    def __str__(self):
        """Chuỗi đại diện cho đối tượng Model."""
        return self.name
from django.urls import reverse  # Được sử dụng để tạo URL bằng cách đảo ngược các mẫu URL

class Book(models.Model):
    """Model đại diện cho một cuốn sách (không phải một bản sao cụ thể của sách)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Nhập mô tả ngắn gọn về cuốn sách')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='Số ISBN 13 ký tự')
    genre = models.ManyToManyField(Genre, help_text='Chọn thể loại cho sách này')

    def __str__(self):
        """Chuỗi đại diện cho đối tượng Model."""
        return self.title

    def get_absolute_url(self):
        """Trả về URL để truy cập bản ghi chi tiết cho sách này."""
        return reverse('book-detail', args=[str(self.id)])
import uuid  # Cần thiết cho các instance sách duy nhất

class BookInstance(models.Model):
    """Model đại diện cho một bản sao cụ thể của một cuốn sách (tức là có thể được mượn từ thư viện)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID duy nhất cho bản sách cụ thể này trong toàn bộ thư viện')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Bảo trì'),
        ('o', 'Đang mượn'),
        ('a', 'Có sẵn'),
        ('r', 'Đặt trước'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Tình trạng sách',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """Chuỗi đại diện cho đối tượng Model."""
        return f'{self.id} ({self.book.title})'
class Author(models.Model):
    """Model đại diện cho một tác giả."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Trả về URL để truy cập một instance tác giả cụ thể."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Chuỗi đại diện cho đối tượng Model."""
        return f'{self.last_name}, {self.first_name}'
