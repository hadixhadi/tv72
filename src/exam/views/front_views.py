from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from exam.models import Exam
from exam.serializers.front_serializer import *
class ExamsList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        all_exam=Exam.objects.all()
        ser_data=ExamModelSerializer(instance=all_exam,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)


class RegisterExam(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,exam_id):
        with transaction.atomic():
            user=request.user
            exam=Exam.objects.get(id=exam_id)
            if not RegisteredExam.objects.filter(user=user, exam=exam).exists():
                register_exam=RegisteredExam.objects.create(
                    exam=exam,
                    user=user
                )
                register_exam.is_active=True
                register_exam.save()
                return Response("exam created successfully",status=status.HTTP_201_CREATED)
            return Response("user already registered this exam",status=status.HTTP_400_BAD_REQUEST)



class StartExam(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,exam_id):
        user = request.user
        if RegisteredExam.objects.filter(user=user, exam__id=exam_id).exists():
            exam=Exam.objects.get(id=exam_id)
            ser_data=StartExamSerializer(instance=exam)
            return Response(ser_data.data,status=status.HTTP_200_OK)
