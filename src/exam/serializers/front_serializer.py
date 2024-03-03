from rest_framework import serializers
from exam.models import *



class ExamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exam
        fields='__all__'




