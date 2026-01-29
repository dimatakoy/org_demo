from datetime import datetime

import pytest

from ninja.testing import TestClient
from .api import employees_router, departments_router
from .models import Employee, Department

# mock real database
pytestmark = [pytest.mark.django_db]

employees_client = TestClient(employees_router)
departments_client = TestClient(departments_router)


@pytest.fixture
def demo_employee():
    return Employee.objects.create(
        first_name="Ivan",
        last_name="Ivanov",
        amount="200",
        hire_date=datetime.now(),
    )


@pytest.fixture
def demo_department():
    return Department.objects.create(title="Test department")


def test_get_employee(demo_employee):
    pk = demo_employee.pk

    response = employees_client.get(f"/{pk}")

    assert response.status_code == 200
    assert response.data["id"] == pk


def test_get_employee_not_found():
    pk = -1

    response = employees_client.get(f"/{pk}")

    assert response.status_code == 410

    assert response.data["ok"] == False
    assert response.data["error_code"] == "employee_not_found"


def test_list_employees(demo_employee):
    response = employees_client.get("/")

    assert response.status_code == 200

    # we need check the shape of response, because we did not provide own schema
    # we does not check limit-offset as its provided by ninja.paginated
    assert response.data["count"] == 1
    assert type(response.data["items"]) is list


def test_get_department(demo_department):
    pk = demo_department.pk
    response = departments_client.get(f"/{pk}")

    assert response.status_code == 200
    assert response.data["id"] == pk


def test_get_department_not_found():
    pk = -1

    response = departments_client.get(f"/{pk}")

    assert response.status_code == 410

    assert response.data["ok"] == False
    assert response.data["error_code"] == "department_not_found"


def test_list_departments():
    response = departments_client.get("/")

    assert response.status_code == 200

    assert response.data["count"] == 0
    assert type(response.data["items"]) is list
