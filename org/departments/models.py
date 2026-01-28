from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Employee(BaseModel):
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=100,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=100,
        blank=False,
        null=False,
    )

    middle_name = models.CharField(
        verbose_name="Отчество",
        max_length=100,
        blank=True,
        null=True,
    )

    amount = models.DecimalField(
        verbose_name="Размер зарплаты",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Сумма в рублях",
    )

    hire_date = models.DateField(
        verbose_name="Дата приёма на работу",
        blank=False,
        null=False,
    )
