from django.contrib import admin
from django.urls import path
from .views import *

 

urlpatterns = [
    path('exams/', ExamListView.as_view(), name='exam-list'),
    path('exams/<uuid:exam_id>/', ExamDetailView.as_view(), name='exam-detail'),
    path('questions/<uuid:qid>/', QuestionByQidView.as_view(), name='question-by-qid'),
    path('exam-attempts/', StartExamAttemptView.as_view(), name='start-attempt'),
    path('exam-attempts/<uuid:attempt_id>/', AttemptDetailView.as_view(), name='attempt-detail'),
    path('exam-attempts/<uuid:attempt_id>/submit/', SubmitExamAttemptView.as_view(), name='submit-attempt'),
    path('exams/<uuid:exam_id>/questions/',ExamQuestionsView.as_view(),name='exam-questions'
)

]