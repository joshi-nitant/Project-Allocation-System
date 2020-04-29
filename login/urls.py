from django.conf.urls import url
from login import views

app_name = 'login'

urlpatterns = [
     url(r'^$',views.index,name='index')
]
