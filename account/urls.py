from django.urls import path

from . import views

app_name= 'account'

urlpatterns = [
    path('dashboard', views.dashboard , name='dashboard'),
    path('login', views.sigin, name='login'),
    path('login_api', views.authenticate_user_api, name='login-api'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('inactive_dashboard', views.in_active_dashboard, name="inactive_dashboard"),
]
