
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import include,path

from .views import questionRudView, questionApiView

urlpatterns = [
    url(r'^$', questionApiView.as_view(),name='question-api'),
    url(r'^(?P<pk>\d+)/$', questionRudView.as_view(),name='question-rud'),

]
app_name='quiz_api'