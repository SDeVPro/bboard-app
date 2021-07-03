from django import template
from django.urls import path
from .views import index,other_page,BBLoginView,profile,BBLogoutView, ChangeUserInfoView, BBPasswordChangeView,RegisterUserView, RegisterDoneView,user_activate
from django.contrib.auth.views import LoginView
app_name = 'main'
urlpatterns = [
    path('<str:page>/',other_page, name='other'),
    path('',index,name='index'),
    path('accounts/profile/',profile,name='profile'),
    path('accounts/logout/',BBLogoutView.as_view(),name='logout'),
    path('accounts/login/',BBLoginView.as_view(),name='login'),
    path('accountss/login/',LoginView.as_view(template_name='main/loginn.html'),name='loginn'),
    path('accounts/profile/change/',ChangeUserInfoView.as_view(),name='profile_change'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(),name='password_change'),
    path('accounts/register/done/',RegisterDoneView.as_view(),name='register_done'),
    path('accounts/register/',RegisterUserView.as_view(),name='register'),
    path('accounts/register/activate/<str:sign>/',user_activate,name='register_activate'),
]