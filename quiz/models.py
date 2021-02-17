# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class QuestionType(models.Model):
	question_type=models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return (str(self.question_type))

class QuestionCategory(models.Model):
	question_category=models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return (str(self.question_category))

class AnswerType(models.Model):
	answer_type=models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return (str(self.answer_type))

class Question(models.Model):
	# question_type_choices=(('text','text'),('image','image'))
	# category_choices=(('coding','coding'),('aptitude','aptitude'),)
	# answer_type_choices=(('text','text'),('choice','choice'),('code','code'))

	# test = models.ForeignKey(Test, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(auto_now=True,null=True, blank=True)
	# category = models.CharField(max_length=200, null=True, blank=True,choices=category_choices)
	question_category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE,null=True, blank=True)
	mark_multiplier = models.IntegerField(null=True, blank=True)

	question_type = models.ForeignKey(QuestionType, on_delete=models.CASCADE,null=True, blank=True)
	question_text = models.TextField(blank=True, null=True)
	question_image_url = models.TextField(blank=True, null=True)



	hint = models.TextField(blank=True, null=True)
	# answer_type = models.CharField(max_length=200, null=True, blank=True,choices=answer_type_choices)
	answer_type = models.ForeignKey(AnswerType, on_delete=models.CASCADE,null=True, blank=True)
	answer_text = models.TextField(blank=True, null=True)
	answer_choice = models.IntegerField(null=True, blank=True)

	starter_code = models.TextField(blank=True, null=True)
	test_case_1 = models.TextField(blank=True, null=True)
	test_case_2 = models.TextField(blank=True, null=True)
	test_case_3 = models.TextField(blank=True, null=True)
	test_case_4 = models.TextField(blank=True, null=True)

	def __str__(self):
		return (str(self.id))

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,null=True, blank=True)
    choice = models.CharField(max_length=200, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = [
            # no duplicated choice per question
            ("question", "choice"), 
            # no duplicated position per question 
            ("question", "position") 
        ]
        ordering = ("position",)

class Test(models.Model):
	test_name = models.CharField(max_length=200, null=True, blank=True)
	no_of_questions_dict = models.TextField(blank=True, null=True)
	# ex:{'coding':{'1':1,'2':2,'3':1},'aptitude':{'1':2,'2':1,'3':2}}
	total_marks = models.IntegerField(null=True, blank=True)
	duration=models.CharField(max_length=200, null=True, blank=True)
	def __str__(self):
		return self.test_name


class TestTakers(models.Model):
	test_taker_category_choices=(('email','email'),('gridlex','gridlex'))

	
	user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
	username = models.CharField(max_length=200, null=True, blank=True)
	test_taker_category = models.CharField(max_length=200, null=True, blank=True,choices=test_taker_category_choices)
	test = models.ForeignKey(Test, on_delete=models.CASCADE,blank=True, null=True)
	total_correct_answers = models.IntegerField(default=0,blank=True, null=True)
	marks_result = models.IntegerField(default=0,blank=True, null=True)
	completed = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True,blank=True, null=True)
	def __str__(self):
		return (str(self.username))



class Response(models.Model):
	test_taker = models.ForeignKey(TestTakers, on_delete=models.CASCADE,blank=True, null=True)
	test = models.ForeignKey(Test, on_delete=models.CASCADE,blank=True, null=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE,blank=True, null=True)
	response = models.TextField(blank=True, null=True)
	is_correct = models.BooleanField(default=False)
	timestamp = models.DateTimeField(blank=True, null=True)
	user_code = models.TextField(blank=True, null=True)


class GeneratedTests(models.Model):
	questions_dict = models.TextField(blank=True, null=True)
	# ex:{'coding':[1,4,8,7],'aptitude':[2,3,6],'type':[ids,,,]}
	test = models.ForeignKey(Test, on_delete=models.CASCADE,blank=True, null=True)
	test_taker = models.ForeignKey(TestTakers, on_delete=models.CASCADE,blank=True, null=True)
	test_start_time = models.DateTimeField(blank=True, null=True)
	test_end_time = models.DateTimeField(blank=True, null=True)



