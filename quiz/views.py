# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random,json

from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from quiz.forms import UserForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from quiz.models import *
from datetime import datetime,timedelta
import pytz,os
from django.views.static import serve


# from django.core.context_processors import csrf

# from rest_framework import viewsets

# from quiz.serializers import ResponseSerializer



def app_static_serve(request, path, document_root=None, show_indexes=False):
	dirpath = os.path.join('/home/ubuntu/Ace/templates/images/')
	print (dirpath,path)
	return serve(request, path, dirpath, show_indexes)


# Create your views here.
@login_required
def test_index(request):
	url_path=request.path
	test_objs=Test.objects.all()
	tests={}
	for test in test_objs:
		tests[str(test.id)]=str(test.test_name)

	# print(tests)

	return render(request,'quiz/test_index.html',locals())

@login_required
def generate_test(request):
	user_obj=request.user
	url_path=request.path

	try:
		test_taker_obj = TestTakers.objects.get(user=user_obj)
		test_name=test_taker_obj.test.test_name
	except:
		test_taker_obj = None
		test_name = None


	if test_name==None:	
		if request.method=='POST' :
			test_name=request.POST.get('test', None)
			test_obj=Test.objects.get(test_name=test_name)
		else:
			# test_name='beginner'
			test_obj=Test.objects.all()[0]
			test_name=test_obj.test_name
		# print ('test_name saving',test_name)
		try:
		    test_obj=Test.objects.get(test_name=test_name)
		except :
		    test_obj= None

		if test_obj:
			test_taker_obj=TestTakers.objects.create(
				user=user_obj,username=user_obj.username,test=test_obj)
			test_taker_obj.save()
			print()

	else:
		pass



	# print("test_name",test_name)
	test_obj=test_taker_obj.test
	
	try:
		generated_test_obj=GeneratedTests.objects.get(test_taker=test_taker_obj)
		# print(generated_test_obj.id, "exists")
	except:
		generated_test_obj=None

	if generated_test_obj==None:
		no_of_questions_dict=json.loads(test_obj.no_of_questions_dict)
		# print(type(no_of_questions_dict))
		print (test_obj.no_of_questions_dict)
		questions_dict={}
		for category in no_of_questions_dict.keys():
			category_dict=no_of_questions_dict[category]
			questions_dict[str(category)]=[]
			for mark in category_dict.keys():
				no_of=category_dict[mark]
				questions=Question.objects.filter(category=category,mark_multiplier=int(mark))
				question_ids=list(map(lambda a:a.id,questions))

				# question_ids=random.sample(question_ids,int(no_of))
				question_ids=sorted(question_ids[:no_of])		

				questions_dict[str(category)].extend(question_ids)
		questions_dict = json.dumps(questions_dict)
		print(questions_dict)
		generated_test_obj=GeneratedTests.objects.create(
			questions_dict=questions_dict,test=test_obj,
			test_taker=test_taker_obj,)
		generated_test_obj.save()
	if generated_test_obj.test_start_time:
		return HttpResponseRedirect(reverse('quiz:start'))

	test_duration=int(test_obj.duration)/60
	return render(request,'quiz/test_index.html',locals())


@login_required
def start(request):
	user_obj=request.user
	url_path=request.path
	try:
		test_taker_obj = TestTakers.objects.get(user=user_obj)
		test_name=test_taker_obj.test.test_name
	except:
		test_taker_obj = None
	test_obj=test_taker_obj.test

	if test_taker_obj.completed==True:
		return HttpResponseRedirect('/quiz/end/')

	try:
		generated_test_obj=GeneratedTests.objects.get(test_taker=test_taker_obj)
		# print(generated_test_obj.id, "exists")
	except:
		generated_test_obj=None
	if generated_test_obj==None:
		return HttpResponseRedirect('/quiz/generate/')
	if generated_test_obj.test_start_time==None or generated_test_obj.test_start_time==None:
		# datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)
		test_duration=int(test_obj.duration)

		start_time_obj = datetime.utcnow()
		start_time_obj=start_time_obj.replace(tzinfo = pytz.utc)

		end_time_obj = start_time_obj+timedelta(seconds=test_duration)
		end_time_obj=end_time_obj.replace(tzinfo = pytz.utc)

		setattr(generated_test_obj,'test_start_time',start_time_obj)
		setattr(generated_test_obj,'test_end_time',end_time_obj)

		generated_test_obj.save()

	# print("test_start_time",generated_test_obj.test_start_time)
	start_time=generated_test_obj.test_start_time
	current_time=datetime.now()
	current_time=current_time.replace(tzinfo = pytz.utc)
	end_time=generated_test_obj.test_end_time
	# print(current_time.tzinfo,end_time.tzinfo)
	# time_left=(end_time-current_time).seconds
	time_left=int((end_time-current_time).total_seconds())
	time_left_mins=time_left/60
	time_left_secs=time_left%60
	# print('time_left',time_left,current_time,	end_time)
	if time_left<=0:
		return HttpResponseRedirect('/quiz/end/')


	questions_dict=json.loads(generated_test_obj.questions_dict)

	questions_lengths={}
	for key in questions_dict:
		questions_lengths[str(key)]=len(questions_dict[key])
	# questions_lengths=questions_lengths.items()
	# print(questions_dict,questions_lengths)

	# category=questions_dict.keys()[0]
	# question_index=1

	# question_number=questions_dict[category][int(question_index)-1]
	# try:
	# 	loaded_question=Question.objects.get(pk=question_number)
	# 	# options=[]
	# 	if loaded_question.question_type=='text':
	# 		question_text=loaded_question.question_text
	# 		question_id=loaded_question.id
	# 	else:
	# 		question_id=None
	# 		pass
	# 	answer_type=loaded_question.answer_type
	# 	if answer_type=='choice':
	# 		options=list(filter(None,[loaded_question.option1,loaded_question.option2,loaded_question.option3,loaded_question.option4,loaded_question.option5]))
	# 		print(options)
	# 	elif answer_type=='text':
	# 		pass
	# except Exception as e:
	# 	print(e)
	# 	pass

	

	return render(request,'quiz/test_page.html',locals())


def get_question(request):
	user_obj=request.user
	url_path=request.path
	if request.POST:
		category=request.POST.get('category')
		question_index=request.POST.get('question_index')
		# print(category,question_index)
	else:
		category='coding'
		question_index=1
	try:
		test_taker_obj = TestTakers.objects.get(user=user_obj)
		test_name=test_taker_obj.test.test_name
	except:
		test_taker_obj = None
	test_obj=test_taker_obj.test
	try:
		generated_test_obj=GeneratedTests.objects.get(test_taker=test_taker_obj)
		# print(generated_test_obj.id, "exists")
	except:
		generated_test_obj=None
	if generated_test_obj==None:
		return HttpResponseRedirect('/quiz/generate/')
	# questions=
	questions_dict=json.loads(generated_test_obj.questions_dict)

	questions_lengths={}
	for key in questions_dict:
		questions_lengths[str(key)]=len(questions_dict[key])

	question_number=questions_dict[category][int(question_index)-1]
	# print(question_number,'question_number')
	try:
		loaded_question=Question.objects.get(pk=question_number)
		# options=[]
		if loaded_question.question_type=='text':
			question_text=loaded_question.question_text
			question_id=loaded_question.id
			image_url=loaded_question.question_image_url

		elif loaded_question.question_type=='image':
			question_text=loaded_question.question_text
			image_url=loaded_question.question_image_url
			question_id=loaded_question.id

		answer_type=loaded_question.answer_type
		starter_code=loaded_question.starter_code
		try:
			marks=loaded_question.mark_multiplier
		except:
			marks=None

		if answer_type=='choice':
			options=list(filter(None,[loaded_question.option1,loaded_question.option2,loaded_question.option3,loaded_question.option4,loaded_question.option5]))
			# print(options)
			try:
				response_obj=Response.objects.get(
					test_taker=test_taker_obj,test=test_obj,question=loaded_question)
				option_response=response_obj.response
				answer_text=response_obj.response
				user_code=response_obj.user_code
			except:
				response_obj=None
				option_response=None
				answer_text=None
				user_code=None

			# print('selected_option',option_response,question_id)

		elif answer_type=='text' or 'code':
			options=None
			try:
				response_obj=Response.objects.get(
					test_taker=test_taker_obj,test=test_obj,question=loaded_question)
				option_response=response_obj.response
				answer_text=response_obj.response
			except:
				response_obj=None
				option_response=None
				answer_text=None
			try:
				user_code=response_obj.user_code
			except:
				user_code=None

	except Exception as e:
		print(e)
		pass
	# options=None
	output_data=json.dumps({'options':options,'question_text':question_text,'option_response':option_response,'question_id':question_id,'image_url':image_url,'answer_type':answer_type,'answer_text':answer_text,'marks':marks,'user_code':user_code,'starter_code':starter_code})
	return(HttpResponse(output_data))

def save_response(request):
	user_obj=request.user
	url_path=request.path
	try:
		test_taker_obj = TestTakers.objects.get(user=user_obj)
		test_name=test_taker_obj.test.test_name
	except:
		test_taker_obj = None
	test_obj=test_taker_obj.test
	try:
		generated_test_obj=GeneratedTests.objects.get(test_taker=test_taker_obj)
		# print(generated_test_obj.id, "exists")
	except:
		generated_test_obj=None
	if generated_test_obj==None:
		return HttpResponseRedirect('/quiz/generate/')
	# questions=
	questions_dict=json.loads(generated_test_obj.questions_dict)

	state='Saved'
	question_id=request.POST.get('question_id')
	selected_response=request.POST.get('selected_response')
	user_code=request.POST.get('user_code')
	print('question_id',question_id,'selected_response',selected_response)

	try:
		question_obj=Question.objects.get(pk=question_id)
		response_obj=Response.objects.get(
			test_taker=test_taker_obj,test=test_obj,question=question_obj)
	except:
		response_obj=None

	if response_obj==None:
		question_obj=Question.objects.get(pk=question_id)
		response_obj=Response.objects.create(
			test_taker=test_taker_obj,test=test_obj,question=question_obj,response=selected_response,user_code=user_code)
		state='saved'
	else:
		setattr(response_obj,'response',selected_response)
		if user_code:
			setattr(response_obj,'user_code',user_code)
		response_obj.save()
		state='changed'

	return(HttpResponse(state))





@login_required
def end_test(request):
	user_obj=request.user
	url_path=request.path
	try:
		test_taker_obj = TestTakers.objects.get(user=user_obj)
		test_name=test_taker_obj.test.test_name
	except:
		test_taker_obj = None
	test_obj=test_taker_obj.test
	try:
		generated_test_obj=GeneratedTests.objects.get(test_taker=test_taker_obj)
		# print(generated_test_obj.id, "exists")
	except:
		generated_test_obj=None
	if generated_test_obj==None:
		return HttpResponseRedirect('/quiz/generate/')

	try:
		if test_taker_obj.completed==False:
			setattr(test_taker_obj,'completed',True)
			test_taker_obj.save()			
		
	except Exception as e:
		print (e)
		pass
	test_taker_obj
	responses=Response.objects.filter(test_taker=test_taker_obj,test=test_obj)
	marks=0
	no_of_correct_answers=0
	for response_obj in responses:
		question_obj=response_obj.question
		answer_type=question_obj.answer_type
		if answer_type=='choice':
			user_response=response_obj.response
			correct_answer=question_obj.answer_choice

			is_correct=str(correct_answer).rstrip().replace('\r', '')==str(user_response).rstrip().replace('\r', '')
			# print(str(correct_answer).rstrip().replace('\r', '')==str(user_response).rstrip().replace('\r', ''))
		elif answer_type=='text' :
			user_response=response_obj.response
			correct_answer=question_obj.answer_text

			is_correct=str(correct_answer).rstrip().replace('\r', '')==str(user_response).rstrip().replace('\r', '')
		elif answer_type=='code':
			user_response=response_obj.response
			correct_answer=question_obj.answer_text

			user_code=response_obj.user_code
			testcases=[]
			if question_obj.test_case_1:
				testcases.append(question_obj.test_case_1)
			if question_obj.test_case_2:
				testcases.append(question_obj.test_case_2)
			if question_obj.test_case_3:
				testcases.append(question_obj.test_case_3)
			if question_obj.test_case_4:
				testcases.append(question_obj.test_case_4)
			try:
				exec(user_code)
			except:
				pass
			testcases_results=[]
			if testcases:
				for testcase in testcases:
					try:
						res=eval(testcase)
					except:
						res=False
					testcases_results.append(res)
				if all(testcases_results):
					is_correct=True
					print('all')
				else:
					is_correct=False
			else:
				is_correct=str(correct_answer).rstrip().replace('\r', '')==str(user_response).rstrip().replace('\r', '')


			# print('user_code',user_code,testcases_results)

		else:
			is_correct=None

		if is_correct:
			marks += int(question_obj.mark_multiplier)
			no_of_correct_answers += 1

		setattr(response_obj,'is_correct',is_correct)
		response_obj.save()

	setattr(test_taker_obj,'total_correct_answers',no_of_correct_answers)
	setattr(test_taker_obj,'marks_result',marks)
	test_taker_obj.save()



	print('marks',marks,'no_of_correct_answers',no_of_correct_answers)
	return render(request,'quiz/result_page.html',locals())



# def evaluate(request):
# 	user_obj=request.user
# 	url_path=request.path
# 	try:
# 		test_taker_obj = TestTakers.objects.get(user=user_obj)
# 		test_name=test_taker_obj.test.test_name
# 	except:
# 		test_taker_obj = None
# 	test_obj=test_taker_obj.test
# 	try:
# 		generated_test_obj=GeneratedTests.objects.get(test_taker=test_taker_obj)
# 		# print(generated_test_obj.id, "exists")
# 	except:
# 		generated_test_obj=None
# 	if generated_test_obj==None:
# 		return HttpResponseRedirect('/quiz/generate/')

# class ResponseViewSet(viewsets.ModelViewSet):
#     queryset = Response.objects.all()	
#     serializer_class = ResponseSerializer
