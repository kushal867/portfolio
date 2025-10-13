from rest_framework import serializers
from .models import Quiz, Question, Choice, UserQuizAttempt, UserAnswer
from django.contrib.auth.models import User


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'marks', 'order', 'explanation', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'difficulty', 'time_limit', 'total_marks', 'random_order', 'is_active', 'created_by', 'created_at', 'updated_at', 'questions']


class UserAnswerSerializer(serializers.ModelSerializer):
    attempt = serializers.PrimaryKeyRelatedField(queryset=UserQuizAttempt.objects.all())
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all())
    selected_choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())

    class Meta:
        model = UserAnswer
        fields = ['id', 'attempt', 'question', 'selected_choice', 'answered_at']

    def create(self, validated_data):
        # Create the UserAnswer and return it
        answer = UserAnswer.objects.create(**validated_data)
        # Recalculate attempt score if desired (defer complex logic to model)
        try:
            attempt = validated_data.get('attempt')
            attempt.calculate_score()
        except Exception:
            pass
        return answer


class UserQuizAttemptSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    answers = UserAnswerSerializer(many=True, required=False)

    class Meta:
        model = UserQuizAttempt
        fields = ['id', 'user', 'quiz', 'score', 'correct_answers', 'incorrect_answers', 'started_at', 'completed_at', 'completed', 'time_taken', 'answers']
