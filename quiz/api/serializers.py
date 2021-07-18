from rest_framework import serializers
from quiz.models import Question

class QuestionSerializer(serializers.ModelSerializer): #forms.ModelForm
    class Meta:
        model = Question
        fields=[
            'pk',
            'pub_date',
            'question_category',
            'mark_multiplier',            
            'question_type',
            'question_text',
            'question_image_url',
            'hint',
            'answer_type',
            'answer_text',
            'answer_choice',
            'starter_code',
            'test_case_1',
            'test_case_2',
            'test_case_3',
            'test_case_4',
        ]
        read_only_fields=['pk','question_category']

    def validate_question(self, value):
        qs = Question.objects.filter(title__iexact=value)
        if self.instance:
            qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("question  must be unique")
        return value