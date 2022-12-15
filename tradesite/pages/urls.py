from django.urls import path
from django.urls import include
from users import views as user_views
from django.contrib.auth import views as auth_views
from . import views
import pandas as pd
import requests
import json


urlpatterns = [
	path('', views.hello, name='hello'),
	path(r'^coin/(?P<parameter>)', views.coin, name="coin"),
	path('portfolio/', views.portfolio, name='port')
]



