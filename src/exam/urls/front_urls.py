from django.urls import path
from exam.views.front_views import *
urlpatterns=[
    path('list/',ExamsList.as_view(),name="exam-list"),
    path('register/<int:exam_id>/',RegisterExam.as_view(),name="register-exam"),
    path('start/<int:exam_id>/',StartExam.as_view(),name="register-exam"),
]