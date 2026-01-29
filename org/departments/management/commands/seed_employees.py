import random
from decimal import Decimal
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from org.departments.models import Department, Position, Employee


class Command(BaseCommand):
    help = "Generates 50,000 employees and 25 hierarchical departments"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Starting data generation..."))

        fake = Faker("ru_RU")

        position_titles = [
            "Генеральный директор",
            "Финансовый директор",
            "CTO",
            "Руководитель отдела",
            "Менеджер проектов",
            "Team Lead",
            "Senior Backend Developer",
            "Middle Backend Developer",
            "Frontend Developer",
            "QA Engineer",
            "DevOps Engineer",
            "HR Специалист",
            "Бухгалтер",
            "Юрист",
            "Офис-менеджер",
        ]

        positions = []
        for title in position_titles:
            pos, _ = Position.objects.get_or_create(title=title)
            positions.append(pos)

        self.stdout.write(self.style.SUCCESS(f"positions: {len(positions)} ready."))

        existing_count = Department.objects.count()
        target_deps = 25

        # Load existing departments into a list to use as potential parents
        departments = list(Department.objects.all())

        if existing_count < target_deps:
            self.stdout.write(
                f"Generating department hierarchy (Target: {target_deps})..."
            )

            with transaction.atomic():
                while len(departments) < target_deps:
                    dep_name = fake.bs().capitalize()

                    parent = None

                    # If we already have departments, try to assign a parent to create hierarchy
                    if departments:
                        # Pick a random potential parent
                        potential_parent = random.choice(departments)

                        # CONSTRAINT: Ensure we don't go deeper than 5 levels.
                        # django-treenode usually provides 'tn_level'.
                        # If the parent is already at level 5, we can't add a child to it.
                        # We also allow creating new Root nodes occasionally (random chance)
                        if potential_parent.tn_level < 5 and random.random() > 0.1:
                            parent = potential_parent

                    # Create the department
                    dep = Department.objects.create(
                        title=dep_name,
                        tn_parent=parent,
                    )
                    departments.append(dep)

        self.stdout.write(
            self.style.SUCCESS(
                f"Departments: {len(departments)} ready (Hierarchy built)."
            )
        )

        TOTAL_EMPLOYEES = 50_000
        BATCH_SIZE = 2000

        self.stdout.write(f"Generating {TOTAL_EMPLOYEES} employees...")

        employees_batch = []
        total_created = 0

        for _ in range(TOTAL_EMPLOYEES):
            # Randomize Salary
            salary = Decimal(random.randint(40_000, 450_000))

            # Randomize Hire Date (within last 5 years)
            days_employed = random.randint(0, 365 * 5)
            hire_dt = date.today() - timedelta(days=days_employed)

            emp = Employee(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.middle_name(),
                amount=salary,
                hire_date=hire_dt,
                position=random.choice(positions),
                department=random.choice(departments),
            )
            employees_batch.append(emp)

            # Flush to DB in batches
            if len(employees_batch) >= BATCH_SIZE:
                Employee.objects.bulk_create(employees_batch)
                total_created += len(employees_batch)
                self.stdout.write(f"   ...created {total_created} employees")
                employees_batch = []

        # Save any remainder
        if employees_batch:
            Employee.objects.bulk_create(employees_batch)
            total_created += len(employees_batch)

        self.stdout.write(
            self.style.SUCCESS(
                f"DONE! Created {total_created} employees distributed in {len(departments)} departments."
            )
        )
