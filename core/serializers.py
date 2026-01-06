# core/serializers.py
from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['qid', 'text', 'points', 'order', 'question_type', 'expected_answer', 'keywords']


class ExamSerializer(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['exam_id', 'title', 'course', 'description', 'duration_minutes', 'max_score']


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.UUIDField(source='question.qid')
    text_answer = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Answer
        fields = ['question', 'text_answer']

class SubmitAnswerSerializer(serializers.Serializer):
    question = serializers.UUIDField()
    text_answer = serializers.CharField()

class SubmitExamAttemptSerializer(serializers.Serializer):
    answers = SubmitAnswerSerializer(many=True)

class ExamQuestionSerializer(serializers.ModelSerializer):
    qid = serializers.UUIDField()

    class Meta:
        model = Question
        fields = ['qid', 'text']

class ExamAttemptSerializer(serializers.ModelSerializer):
    exam = serializers.UUIDField(source='exam.exam_id')
    answers = AnswerSerializer(many=True, read_only=True, allow_empty=True)

    class Meta:
        model = ExamAttempt
        fields = ['attempt_id', 'exam', 'started_at', 'submitted_at', 'score', 'max_possible', 'is_completed', 'answers']
        read_only_fields = ['attempt_id', 'started_at', 'submitted_at', 'score', 'max_possible', 'is_completed', 'answers']