from django.urls import path
from . import views

app_name = 'ponto'

urlpatterns = [
    path('home/',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='signup'),
]