from django.urls import path
from django.conf.urls import url,include

from quiz import views

app_name = 'quiz'

from . import views

urlpatterns= [
# path('',views.index, name='index')
    url(r'^start/$',views.start,name='start'),
    url(r'^end/$',views.end_test,name='end_test'),
    url(r'^question/$',views.get_question),
    url(r'^generate/$',views.generate_test,name='generate'),
    url(r'^save_response/$',views.save_response),
    
    url(r'^$', views.test_index, name='test_index'),
    

    # url(r'^api/', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^question/(?P<category>.*)/(?P<question_index>.*)/$',views.get_question,{}),
]