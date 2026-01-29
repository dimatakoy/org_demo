from datetime import datetime
from typing import List, Literal

from django.db.models import F

from ninja import Router, Schema
from ninja.pagination import paginate, LimitOffsetPagination

from .models import Employee, Department

employees_router = Router()
departments_router = Router()


class EmployeeSchema(Schema):
    id: int

    first_name: str
    last_name: str
    middle_name: str | None

    amount: int
    hire_date: datetime

    position_title: str | None


class EmployeeNotFoundSchema(Schema):
    ok: Literal[False]
    error_code: Literal["employee_not_found"]


class DepartmentSchema(Schema):
    id: int
    title: str
    parent_id: int | None
    children: List["DepartmentSchema"] = []

    @staticmethod
    def resolve_parent_id(obj: Department):
        return obj.get_parent_pk


class DepartmentFoundSchema(Schema):
    ok: Literal[False]
    error_code: Literal["department_not_found"]


@employees_router.get(
    "/{id}",
    response={
        200: EmployeeSchema,
        410: EmployeeNotFoundSchema,
    },
)
def get_employee(request, id: int):
    try:
        employee = (
            Employee.objects.select_related("position")
            .annotate(position_title=F("position__title"))
            .get(pk=id)
        )

        return 200, employee
    except Employee.DoesNotExist:
        return 410, EmployeeNotFoundSchema(ok=False, error_code="employee_not_found")


@employees_router.get("/", response=List[EmployeeSchema])
@paginate(LimitOffsetPagination)
def list_employees(request):
    return (
        Employee.objects.select_related("position")
        .annotate(position_title=F("position__title"))
        .all()
    )


@departments_router.get("/", response=List[DepartmentSchema])
@paginate(LimitOffsetPagination)
def list_departments(request):
    return Department.objects.all()


@departments_router.get(
    "/{id}",
    response={
        200: DepartmentSchema,
        410: DepartmentFoundSchema,
    },
)
def get_department(request, id: int):
    try:
        department = Department.objects.get(pk=id)
        return 200, department
    except Department.DoesNotExist:
        return 410, DepartmentFoundSchema(ok=False, error_code="department_not_found")


@departments_router.get("/{department_id}/employees", response=List[EmployeeSchema])
@paginate(LimitOffsetPagination)
def list_departments_employees(request, department_id: int):
    return (
        Employee.objects.select_related("position")
        .annotate(position_title=F("position__title"))
        .filter(department_id=department_id)
    )
