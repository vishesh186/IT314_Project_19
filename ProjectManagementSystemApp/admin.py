from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
from django_json_widget.widgets import JSONEditorWidget
from django import forms

# Register your models here.

class ProjectForm(forms.ModelForm):
    team = forms.JSONField()
    class Meta:
        model = Project
        fields = "__all__"

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm

admin.site.register(Project, ProjectAdmin)


class EmployeeForm(forms.ModelForm):
    team = forms.JSONField()
    class Meta:
        model = Employee
        fields = "__all__"

class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeForm

admin.site.register(Employee, EmployeeAdmin)


admin.site.register(Team)

admin.site.register(Task)
