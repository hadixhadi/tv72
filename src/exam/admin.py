from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','question']

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



@admin.register(AnswerQuestion)
class AnswerQuestionAdmin(admin.ModelAdmin):
    list_display = ['id','user','question','answer','exam']