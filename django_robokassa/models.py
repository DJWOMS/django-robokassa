from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class AddingFund(models.Model):
    """Модель пополнения"""
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name='Сумма', default=50.00, max_digits=19, decimal_places=2)
    purchase_at = models.DateTimeField(verbose_name='Дата покупки', default=timezone.now)
    is_approved = models.BooleanField(verbose_name='Успех пополнения', default=False)

    class Meta:
        verbose_name: str = 'пополнение'
        verbose_name_plural: str = 'пополнения'

    def __str__(self) -> str:
        return f'{self.pk} - {self.user.username}'


__all__ = ('AddingFund',)
