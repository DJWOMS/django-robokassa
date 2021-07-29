from django.conf.urls import url

from django_robokassa.views import (buy, popoln, success, fail)

urlpatterns = [
    url(regex=r'^buy/$', view=buy, name='buy'),
    url(regex=r'^popoln/$', view=popoln, name='popoln'),
    url(regex=r'^success/$', view=success, name='success'),
    url(regex=r'^fail/$', view=fail, name='fail'),
]
app_name: str = 'django_robokassa'

__all__ = ('app_name', 'urlpatterns',)
