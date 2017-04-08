from django.conf.urls import url
from django-robokassa import views

urlpatterns = [
	url(r'^buy/$', sys_money.buy, name='buy'),
	url(r'^popoln/$', sys_money.popoln, name='popoln'),
	url(r'^success/$', sys_money.success, name='success'),
	url(r'^fail/$', sys_money.fail, name='fail'),
]
