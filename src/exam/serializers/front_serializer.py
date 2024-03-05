from django.db import transaction
from rest_framework import serializers, status
from rest_framework.response import Response

from exam.models import *

class EntryUserSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=get_user_model()
        fields=['first_name']

class ExamModelSerializer(serializers.ModelSerializer):
    user_registered_exams=serializers.SerializerMethodField()
    first_name=serializers.SerializerMethodField()
    class Meta:
        model=Exam
        fields='__all__'

    def get_user_registered_exams(self,obj):
        request=self.context.get('request')
        all_registered_exams=RegisteredExam.objects.filter(user=request.user)
        ser_data=RegisteredExamModelSerializer(instance=all_registered_exams,many=True)
        return ser_data.data
    def get_first_name(self,obj):
        request=self.context.get('request')
        user=request.user
        ser_data=EntryUserSpecificationSerializer(instance=user)
        return ser_data.data
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




class UserAnswerSerializer(serializers.Serializer):
    answers = serializers.DictField()

    def create(self, validated_data):
        with transaction.atomic():
            answers_data = validated_data['answers']
            user_answers = []
            request=self.context.get("request")
            exam_id=self.context.get("exam_id")
            user=request.user
            exam_obj=Exam.objects.get(id=exam_id)
            for question_id,answer_id in answers_data.items():
                question_instance=Question.objects.get(pk=question_id)
                user_answers.append(AnswerQuestion(user=user,exam=exam_obj,
                                                  question=question_instance,answer=answer_id
                                                   ))
            AnswerQuestion.objects.bulk_create(user_answers)
            return Response("done",status=status.HTTP_200_OK)


class RegisteredExamModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredExam
        fields=['exam']