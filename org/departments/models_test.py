import pytest
from decimal import Decimal
from datetime import date
from django.core.exceptions import ValidationError
from django.db import transaction, models
from .models import Employee, Department


# mock real database
pytestmark = [pytest.mark.django_db]


@pytest.fixture
def employee_data():
    return {
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "middle_name": "Ivanovich",
        "amount": Decimal("50000.00"),
        "hire_date": date(2026, 1, 28),
    }


@pytest.fixture
def department_with_employee(employee_data):
    with transaction.atomic():
        department = Department.objects.create(title="Тестовый департамент")
        Employee.objects.create(**employee_data, department=department)
        return department


def test_create_valid_employee(employee_data):
    employee = Employee.objects.create(**employee_data)

    assert Employee.objects.count() == 1
    assert employee.first_name == "Ivan"
    assert employee.amount == Decimal("50000.00")


def test_middle_name_is_optional(employee_data):
    employee_data["middle_name"] = None
    employee = Employee.objects.create(**employee_data)

    assert employee.middle_name is None


@pytest.mark.parametrize("field", ["first_name", "last_name", "hire_date"])
def test_required_fields(employee_data, field):
    employee_data[field] = None
    employee = Employee(**employee_data)

    with pytest.raises(ValidationError) as e:
        employee.full_clean()
        # Verify the error is specifically about the missing field
        assert field in e.value.message_dict


def test_amount_cannot_be_none(employee_data):
    employee_data["amount"] = None
    employee = Employee(**employee_data)

    with pytest.raises(ValidationError):
        employee.full_clean()


@pytest.mark.parametrize("field", ["first_name", "last_name", "middle_name"])
def test_char_fields_max_length(employee_data, field):
    # Create a string with 101 characters
    employee_data[field] = "a" * 101
    employee = Employee(**employee_data)

    with pytest.raises(ValidationError) as e:
        employee.full_clean()

    assert field in e.value.message_dict


def test_amount_min_value_validator(employee_data):
    employee_data["amount"] = Decimal("-10.00")
    employee = Employee(**employee_data)

    with pytest.raises(ValidationError) as e:
        employee.full_clean()

    assert "amount" in e.value.message_dict
    # Check that the error message is related to the limit (optional)
    assert "Ensure this value is greater than or equal to 0.00" in str(
        e.value.message_dict["amount"]
    )


def test_amount_zero_is_allowed(employee_data):
    employee_data["amount"] = Decimal("0.00")
    employee = Employee(**employee_data)
    try:
        employee.full_clean()
    except ValidationError:
        pytest.fail("Amount should allow 0.00")


def test_decimal_places_validation(employee_data):
    """
    Test that providing more than 2 decimal places might cause validation error
    or rounding (depending on DB, but save handles Python level validation).
    """
    # Django's standard DecimalField validation usually checks max_digits
    # and decimal_places.
    employee_data["amount"] = Decimal("100.999")
    employee = Employee(**employee_data)

    with pytest.raises(ValidationError) as e:
        employee.full_clean()

    assert "amount" in e.value.message_dict


def test_cannot_delete_department_with_employee(department_with_employee):
    with pytest.raises(models.deletion.ProtectedError):
        department_with_employee.delete()
