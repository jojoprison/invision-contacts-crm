from django.db import models
import uuid


class Contact(models.Model):
    """
    Каждый контакт существует внутри схемы конкретного арендатора.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, help_text='ФИО контакта')
    email = models.EmailField(unique=True, help_text='Email контакта (уникальный в пределах схемы)')
    phone = models.CharField(
        max_length=20, blank=True, null=True,
        help_text='Телефон контакта (опционально)'
    )
    date_created = models.DateTimeField(auto_now_add=True, help_text='Дата создания')

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        ordering = ['-date_created']
