from django.conf.urls import url
from .forms import UserAuthenticationForm
from .views import register, logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^login/$',  auth_views.login, {
        'template_name': 'account/login.html',
        'authentication_form': UserAuthenticationForm
        },
        name='login', ),
    url(r'^logout/$',  logout_view, {}, name='logout', ),
]