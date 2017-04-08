from django.conf.urls import url
from django-robokassa import views

urlpatterns = [
	url(r'^buy/$', views.buy, name='buy'),
	url(r'^popoln/$', views.popoln, name='popoln'),
	url(r'^success/$', views.success, name='success'),
	url(r'^fail/$', views.fail, name='fail'),
]
