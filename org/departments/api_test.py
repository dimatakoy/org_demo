from datetime import datetime

import pytest

from ninja.testing import TestClient
from .api import employees_router
from .models import Employee

# mock real database
pytestmark = [pytest.mark.django_db]

client = TestClient(employees_router)


@pytest.fixture
def demo_employee():
    return Employee.objects.create(
        first_name="Ivan",
        last_name="Ivanov",
        amount="200",
        hire_date=datetime.now(),
    )


def test_get_employee(demo_employee):
    pk = demo_employee.pk

    response = client.get(f"/{pk}")

    assert response.status_code == 200
    assert response.data["id"] == pk


def test_get_employee_not_found():
    pk = -1

    response = client.get(f"/{pk}")

    assert response.status_code == 410

    assert response.data["ok"] == False
    assert response.data["error_code"] == "employee_not_found"


def test_list_employees(demo_employee):
    response = client.get("/")

    assert response.status_code == 200

    # we need check the shape of response, because we did not provide own schema
    # we does not check limit-offset as its provided by ninja.paginated
    assert response.data["count"] == 1
    assert type(response.data["items"]) is list
