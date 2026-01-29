from django.contrib import admin

from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm

from .models import Employee, Position, Department


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(TreeNodeModelAdmin):
    treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
    form = TreeNodeForm
