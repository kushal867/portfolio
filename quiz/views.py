from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Quiz, Question, Choice, UserQuizAttempt, UserAnswer
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, UserQuizAttemptSerializer, UserAnswerSerializer


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Quiz.objects.filter(is_active=True)
	serializer_class = QuizSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]

	@action(detail=True, methods=['post'], url_path='start')
	def start_quiz(self, request, pk=None):
		quiz = self.get_object()
		# Only authenticated users may start an attempt (permission class enforces this)
		user = request.user
		attempt, created = UserQuizAttempt.objects.get_or_create(user=user, quiz=quiz)
		attempt_serializer = UserQuizAttemptSerializer(attempt)
		quiz_serializer = QuizSerializer(quiz)
		return Response({'attempt': attempt_serializer.data, 'quiz': quiz_serializer.data})


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


class ChoiceViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Choice.objects.all()
	serializer_class = ChoiceSerializer
	permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def submit_answer(request):
	"""Submit an answer for an attempt. Expecting: attempt, question, selected_choice"""
	serializer = UserAnswerSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

