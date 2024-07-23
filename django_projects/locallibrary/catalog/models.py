from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse  
import uuid  
from datetime import date
from constants import LOAN_STATUS
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text=_('Enter a book genre (e.g. Science Fiction)'))

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text=_('Enter a brief description of the book'))
    isbn = models.CharField(_('ISBN'), max_length=13, unique=True, help_text=_('13 character ISBN number'))
    genre = models.ManyToManyField(Genre, help_text=_('Select a genre for this book'))

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('catalog:book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = _('Genre')

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_('Unique ID for this particular book across whole library'))
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book availability'),
    )

    borrower = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='borrowed_books')
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
    date_of_death = models.DateField(_('Died'), null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

