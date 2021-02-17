# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User
from quiz.models import Question,Test, TestTakers,Response,GeneratedTests,QuestionType,QuestionCategory,AnswerType,Choice

# Register your models here.
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(TestTakers)
admin.site.register(Response)
admin.site.register(GeneratedTests)
admin.site.register(QuestionType)
admin.site.register(QuestionCategory)
admin.site.register(AnswerType)
admin.site.register(Choice)