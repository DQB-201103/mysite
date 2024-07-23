from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.models import User
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Nhập thể loại sách (ví dụ: Khoa học viễn tưởng)')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Nhập mô tả ngắn gọn về cuốn sách')
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='Số ISBN 13 ký tự')
    genre = models.ManyToManyField(Genre, help_text='Chọn thể loại cho sách này')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID duy nhất cho bản sách cụ thể này trong toàn bộ thư viện')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrowed_books')
    status = models.CharField(max_length=1, choices=(('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')), default='a')

    LOAN_STATUS = (
        ('m', 'Bảo trì'),
        ('o', 'Đang mượn'),
        ('a', 'Có sẵn'),
        ('r', 'Đặt trước'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Tình trạng sách')

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),)

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
