from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.first, name="first"),

    path('cal_calc',views.cal_calc, name="cal_calc"),
    
    path('login',views.user_login,name="login"),
    
    path('register',views.register,name="register"),

    path('first',views.first,name="first"),
    
    path('profile', views.Hprofile, name='profile'),
    
    path('logout' , views.user_logout , name="logout") ,
    
    path('forget' , views.forget , name="forget") ,
    
    path( 'change_passw/<token>/', views.change_passw , name="change_passw") ,
    
    
    
    
    path('index' , views.ind , name="ind") 
    
    



    ]