from django.urls import path
from django.contrib.auth import views as auth_views 
from .forms import LoginForm  #Import custom user login from form.py 
from .views import (index, user_dashboard, bp_prediction, bp_form, user_setting, history, deletHistory, des_dataset, logout) #Import all the views

urlpatterns = [
    path('', index, name='index_url'),
    path('login/', auth_views.LoginView.as_view(template_name='bp/login.html', authentication_form=LoginForm), name='login'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('user/prediction/', bp_form, name='prediction'),
    path('user/prediction/result/', bp_prediction, name='pred_result'),
    path('user/setting/', user_setting, name='setting'),
    path('user/history/', history, name='history'),
    path('user/delete/history/<int:id>', deletHistory, name='delete_history'),
    path('user/dataset/', des_dataset, name='dataset_desc'),
    path('logout/', logout, name='logout')
]
