from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Exam(models.Model):
    TYPE=[
        (1,'strong'),
    ]
    type=models.SmallIntegerField(choices=TYPE)
    name=models.CharField(max_length=200)
    def __str__(self):
        return f"{self.name}"

class Module(models.Model):
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE,related_name="exam_module")
    name=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return f"{self.name}"

class Question(models.Model):
    TYPE = [
        (1, "Verbal talent"),
        (2, "math talent"),
        (3, "space talent"),
        (4, "Science talent"),
        (5, "music talent"),
        (6, "Sports talent"),
        (7, "Social aptitude")
    ]
    module=models.ForeignKey(Module,on_delete=models.CASCADE,related_name="questions")
    question=models.CharField(max_length=400)
    type=models.SmallIntegerField(choices=TYPE,default=1)

    def __str__(self):
        return f"{self.question}"

    @classmethod
    def get_question_types(cls):
        return cls.TYPE



class RegisteredExam(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name="user_exam")
    exam=models.ForeignKey(Exam,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)