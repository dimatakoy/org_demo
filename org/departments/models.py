from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Position(BaseModel):
    title = models.CharField(verbose_name="Должность", null=False, blank=False)

    def __str__(self):
        return f"{self.pk}#{self.title}"


class Department(BaseModel):
    title = models.CharField(
        verbose_name="Департамент",
        max_length=100,
        blank=False,
        null=False,
    )

    def __str__(self):
        breadcrumbs = [item.title for item in self.breadcrumbs]
        return " / ".join(breadcrumbs)


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

    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        related_name="employees",
        null=True,
        blank=True,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,  # запрещаем удаление отдела, пока в нём есть сотрудники
        related_name="employees",
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.middle_name is None:
            return f"#{self.pk} / {self.last_name} {self.first_name}"

        return f"#{self.pk} / {self.last_name} {self.first_name} {self.middle_name}"
