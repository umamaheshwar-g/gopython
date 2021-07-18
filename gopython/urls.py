"""gopython URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import include,path
from home import signup_views
from home import views as home_views
from quiz import views

urlpatterns = [
    path('',include('home.urls')),
	url(r'^$',home_views.index,name='home'),

    path('admin/', admin.site.urls),
    path('home/',include('home.urls')),
    # path('quiz/',include('quiz.urls')),
    # url(r'^admin/', admin.site.urls),
    url(r'^images/(?P<path>.*)$', views.app_static_serve,name='images'),
	# url(r'^$',signup_views.index,name='signup_index'),
    url(r'^login/$',signup_views.user_login,name='user_login'),
    url(r'^register/$',signup_views.register,name='register'),
    url(r'^special/',signup_views.special,name='special'),
    url(r'^logout/$', signup_views.user_logout, name='logout'),

    url(r'^quiz/', include('quiz.urls')),



    url(r'^api/quiz/', include('quiz.api.urls', namespace='api-quiz')),


]
