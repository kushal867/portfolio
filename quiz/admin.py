from django.contrib import admin
from .models import Quiz, Question, Choice, UserQuizAttempt, UserAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'is_active', 'created_by', 'created_at')
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title',)
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'order', 'marks')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [ChoiceInline]

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('text',)

@admin.register(UserQuizAttempt)
class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed', 'started_at', 'completed_at')
    list_filter = ('quiz', 'completed')
    search_fields = ('user__username', 'quiz__title')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_choice', 'answered_at')
    list_filter = ('attempt', 'question')
    search_fields = ('attempt__user__username', 'question__text')
