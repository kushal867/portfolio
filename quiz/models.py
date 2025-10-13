from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Quiz(models.Model):
    LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=LEVELS, default='medium')
    time_limit = models.DurationField(null=True, blank=True, help_text="hh:mm:ss")
    total_marks = models.PositiveIntegerField(default=0)
    random_order = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='quizzes_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def question_count(self):
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    marks = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True, help_text="Optional: Explain the correct answer")

    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text[:50]}{' ✅' if self.is_correct else ''}"


class UserQuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    incorrect_answers = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    time_taken = models.DurationField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'quiz')
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} | {self.quiz.title}"

    def finish(self):
        self.completed = True
        self.completed_at = timezone.now()
        if self.started_at:
            self.time_taken = self.completed_at - self.started_at
        self.save()

    def calculate_score(self):
        correct = self.answers.filter(selected_choice__is_correct=True).count()
        total_marks = sum(a.question.marks for a in self.answers.filter(selected_choice__is_correct=True))
        incorrect = self.answers.count() - correct
        self.correct_answers = correct
        self.incorrect_answers = incorrect
        self.score = total_marks
        self.finish()


class UserAnswer(models.Model):
    attempt = models.ForeignKey(UserQuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"{self.attempt.user.username} → {self.question.text[:40]}"
