from rest_framework import serializers
from exam.models import *



class ExamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exam
        fields='__all__'


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'
class ExamModuleSerializer(serializers.ModelSerializer):
    questions=serializers.SerializerMethodField()
    class Meta:
        model=Module
        fields='__all__'
    def get_questions(self,obj):
        questions=Question.objects.filter(module__id=obj.id)
        ser_data=QuestionsSerializer(instance=questions,many=True)
        return ser_data.data
class StartExamSerializer(serializers.ModelSerializer):
    module=serializers.SerializerMethodField()
    class Meta:
        model=Exam
        fields='__all__'
    def get_module(self,obj):
        module=Module.objects.filter(exam__id=obj.id)
        ser_data=ExamModuleSerializer(instance=module,many=True)
        return ser_data.data