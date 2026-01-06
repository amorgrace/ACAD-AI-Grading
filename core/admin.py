# core/admin.py
from django.contrib import admin
from .models import Exam, Question, ExamAttempt


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'course',
        'duration_minutes',
        'is_active',
        'created_by',
        'exam_id',            
    )
    list_filter = ('course', 'is_active')
    search_fields = ('title', 'description', 'exam_id')
    readonly_fields = ('exam_id', 'created_by')
    
    fields = (
        'title',
        'course',
        'description',
        'duration_minutes',
        'is_active',
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'text_short',
        'exam',
        'points',
        'order',
        'qid',
        'question_type'
    )
    list_filter = ('exam__course', 'question_type')
    search_fields = ('text', 'qid')
    ordering = ('exam', 'order')

    fieldsets = (
        (None, {
            'fields': ('exam', 'text', 'points', 'order', 'question_type')
        }),
        ('Short Answer Grading', {
            'fields': ('expected_answer', 'keywords'),
            'classes': ('collapse',),
            'description': 'Only used for SHORT type questions'
        }),
        ('Metadata', {
            'fields': ('qid',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('qid',)

    def text_short(self, obj):
        return obj.text[:70] + "..." if len(obj.text) > 70 else obj.text
    text_short.short_description = "Question"

@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'attempt_id',        
        'student',
        'exam',
        'started_at',
        'submitted_at',
        'score',
        'max_possible',
        'is_completed',
    )
    list_filter = (
        'is_completed',
        'exam__course',       
        'started_at',
    )
    search_fields = (
        'student__email',
        'student__first_name',
        'student__last_name',
        'exam__title',
        'attempt_id',         
    )
    readonly_fields = (
        'attempt_id',
        'started_at',
        'submitted_at',
        'score',
        'max_possible',
        'is_completed',
    )
    date_hierarchy = 'started_at'  
    
    fieldsets = (
        ('Student & Exam', {
            'fields': ('student', 'exam')
        }),
        ('Status & Timing', {
            'fields': ('started_at', 'submitted_at', 'is_completed')
        }),
        ('Score', {
            'fields': ('score', 'max_possible')
        }),
        ('Metadata', {
            'fields': ('attempt_id',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        if obj and obj.is_completed:
            return False
        return super().has_change_permission(request, obj)
    