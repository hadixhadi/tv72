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
        ser_data=ExamModelSerializer(instance=all_exam,many=True,context={'request':request})
        return Response(ser_data.data,status=status.HTTP_200_OK)


class RegisterExam(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,exam_id):
        with transaction.atomic():
            user=request.user
            exam=Exam.objects.get(id=exam_id)
            modules=Module.objects.filter(exam__id=exam_id)
            module_ser=ModuleIdModelSerializer(instance=modules,many=True)
            if not RegisteredExam.objects.filter(user=user, exam=exam).exists():
                register_exam=RegisteredExam.objects.create(
                    exam=exam,
                    user=user
                )
                register_exam.is_active=True
                register_exam.save()

                return Response(module_ser.data,status=status.HTTP_201_CREATED)
            return Response(module_ser.data,status=status.HTTP_403_FORBIDDEN)



class StartExam(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,exam_id,module_id):
        user = request.user
        try:
            if RegisteredExam.objects.filter(user=user, exam__id=exam_id).exists():
                # exam=Exam.objects.get(id=exam_id)
                module=Module.objects.get(exam__id=exam_id,id=module_id)
                ser_data=ExamModuleSerializer(instance=module,context={'request':request})
                # ser_data=StartExamSerializer(instance=exam,context={"request":request})
                return Response(ser_data.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_400_BAD_REQUEST)





class CommitExam(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,exam_id):
        """
        show questions of exam
        this means user entered in dashboard as parent user:
        `request.session['current_user_child'] == None:`
        :param request:
        :param course_id: id of course that user can check
        :return:
        """

        if RegisteredExam.objects.filter(user=request.user,exam__id=exam_id).exists():
            ser_data=UserAnswerSerializer(data=request.data,context={'request':request,
                                                                     'exam_id':exam_id})
            if ser_data.is_valid():
                ser_data.create(ser_data.validated_data)
                if ser_data.validated_data['is_complete']==True:
                    registered_exam=RegisteredExam.objects.get(user=request.user,exam__id=exam_id)
                    registered_exam.is_active=False
                    registered_exam.save()


            else:
                return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)

            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response("exam not valid!",status=status.HTTP_400_BAD_REQUEST)




