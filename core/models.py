from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()

class Exam(models.Model):
    exam_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=20, choices=User.COURSE_CHOICES, db_index=True)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveSmallIntegerField(default=60)
    is_active = models.BooleanField(default=True, db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    max_score = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return f"{self.title} ({self.course})"


class Question(models.Model):
    QUESTION_TYPES = (
        ('SHORT', 'Short Answer'),
    )

    qid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', db_index=True)
    text = models.TextField()
    points = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='SHORT', db_index=True)
    expected_answer = models.TextField(blank=True)
    keywords = models.JSONField(default=list, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['exam', 'order']),
        ]

    def __str__(self):
        return f"Q{self.order}: {self.text[:60]}..."

class ExamAttempt(models.Model):
    attempt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attempts', db_index=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attempts', db_index=True)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveSmallIntegerField(null=True, blank=True)
    max_possible = models.PositiveSmallIntegerField(null=True)
    is_completed = models.BooleanField(default=False, db_index=True)

    class Meta:
        unique_together = ['student', 'exam']
        indexes = [
            models.Index(fields=['student', 'exam']),
        ]

    def __str__(self):
        return f"{self.student.email} - {self.exam.title}"
    
    def grade(self):
        from .services.grading import GradingService
        return GradingService.update_attempt_score(self)


class Answer(models.Model):
    answer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(ExamAttempt, on_delete=models.CASCADE, related_name='answers', to_field='attempt_id', db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_index=True)
    text_answer = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['attempt', 'question']),
        ]

    def __str__(self):
        return f"Answer to Q{self.question.order} by {self.attempt.student}"