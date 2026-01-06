# core/views.py
from rest_framework import generics, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from core.services.grading import GradingService
from drf_yasg.utils import swagger_auto_schema

from django.shortcuts import get_object_or_404



class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: Use this endpoint to get all active exams."
        ))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.filter(is_active=True)
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'exam_id'
    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: Use this endpoint to get an active exam by id."
        ))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class QuestionByQidView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: Use this endpoint to get a question."
        ))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get(self, request, qid):
        try:
            question = Question.objects.get(qid=qid)
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(
                {"error": "Question not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
class ExamQuestionsView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description=(
            "💡 **Tester Note:** Retrieve all questions and their IDs for a specific exam. "
            "Use these question IDs when submitting your answers via `/core/exam-attempts/{attempt_id}/submit/`."
        ),
        responses={200: ExamQuestionSerializer(many=True)}
    )
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        questions = exam.questions.all()

        serializer = ExamQuestionSerializer(questions, many=True)
        return Response({
            "exam_id": exam.exam.id, 
            "questions": serializer.data
        })


class StartExamAttemptView(generics.CreateAPIView):
    serializer_class = ExamAttemptSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: Use this endpoint to start an exam attempt, you will get a metadata with id needed when submitting your answers via `/core/exam-attempts/{attempt_id}/submit/`."
        ))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        exam_id = self.request.data.get("exam")

        if not exam_id:
            raise ValidationError({"exam": "Exam ID is required"})
        
        exam = get_object_or_404(Exam, exam_id=exam_id, is_active=True)

        if ExamAttempt.objects.filter(student=self.request.user, exam=exam).exists():
            raise ValidationError({"detail": "You have already started or completed this exam"})

        serializer.save(student=self.request.user, exam=exam)



    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: Use this endpoint to start an exam attempt, you will get a metadata with id needed when submitting your answers via `/core/exam-attempts/{attempt_id}/submit/`."
        ))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
class SubmitExamAttemptView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description=(
            "💡 **Tester Note:** Submit your exam answers. "
            "You must include the correct question IDs for each answer. "
            "The exam-attempt ID is in the box below"
            "\n\n**Format:** Provide an array of answer objects, each containing 'question' (ID) and 'text_answer'."
        ),
        request_body=SubmitExamAttemptSerializer,
        responses={
            200: ExamAttemptSerializer,
            400: "Invalid input data",
            404: "Exam attempt not found"
        }
    )
    
    def post(self, request, attempt_id):
        attempt = get_object_or_404(ExamAttempt, attempt_id=attempt_id, student=request.user)

        if attempt.is_completed:
            return Response({"detail": "Already submitted"}, status=403)

        answers_data = request.data.get("answers", [])

        if not answers_data:
            return Response({"detail": "No answers provided"}, status=400)

        for ans in answers_data:
            question_uuid = ans.get("question")
            if not question_uuid:
                continue

            question = get_object_or_404(Question, qid=question_uuid, exam=attempt.exam)

            text_answer = ans.get("text_answer", "")
            Answer.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={'text_answer': text_answer}
            )


        attempt.is_completed = True
        attempt.submitted_at = timezone.now()
        GradingService.update_attempt_score(attempt)
        attempt.save(update_fields=['is_completed', 'submitted_at'])

        serializer = ExamAttemptSerializer(attempt)
        return Response(serializer.data, status=200)


class AttemptDetailView(generics.RetrieveAPIView):
    serializer_class = ExamAttemptSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'attempt_id'
    @swagger_auto_schema(
        operation_description=(
            "💡 Tester Note: Users can check their submitted exams here"
        ))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

    def get_queryset(self):
        return ExamAttempt.objects.filter(student=self.request.user)