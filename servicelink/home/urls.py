from django.urls import path,include
from django.contrib.auth.views import LogoutView
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('service', views.service, name='service'),
    path('booking', views.booking),
    path('login', views.user_login, name='login'),
    path('signup', views.signup, name='signup'),
    path('providersignup', views.providersignup, name='providersignup'),
    path('providerlogin', views.providerlogin, name='providerlogin'),
     path('logout/', views.user_logout, name='logout'),  # ✅ Custom logout
     path('providerlogout/', views.provider_logout, name='provider_logout'),
]