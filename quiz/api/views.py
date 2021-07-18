# generic views  (meaning they are suitable for common use case patterns)
# Create List Retrieve Destroy Update


from rest_framework import generics
from quiz.models import Question
from .serializers import QuestionSerializer

class questionApiView(generics.CreateAPIView):
    lookup_field='pk'
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()

class questionRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field='pk'
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()



