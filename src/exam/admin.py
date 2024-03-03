from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Exam)




class QuestionInline(admin.TabularInline):
    model = Question
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id','name','exam']
    inlines=[
        QuestionInline
    ]

@admin.register(RegisteredExam)
class RegisteredExamAdmin(admin.ModelAdmin):
    list_display = ['user','exam','is_active','created_at']