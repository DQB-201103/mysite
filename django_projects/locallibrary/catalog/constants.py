from django.utils.translation import gettext_lazy as _
PAGINATE_BY = 10
CONTEXT_OBJECT_NAME = 'my_book_list'

LOAN_STATUS = (
        ('m', _('Maintenance')),
        ('o', _('On loan')),
        ('a', _('Available')),
        ('r', _('Reserved')),
    )

