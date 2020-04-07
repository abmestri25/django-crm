
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
     
    
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutPage,name="logout"),

    path('register/',views.registerPage,name="register"),
    path('',views.home,name="home"),
    path('product/',views.product,name="product"),
    path('settings/',views.setting,name="settings"),
    path('user/',views.userPage,name="user"),
    path('customer/<str:pk>/',views.customer,name="customer"),
    path('create_order/<str:pk>/',views.create_order,name="create_order"),
    path('update_order/<str:pk>/',views.update_order,name="update_order"),
    path('delete_order/<str:pk>/',views.delete_order,name="delete_order"),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),name="password_reset") ,

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_done") ,

    path('reset_password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm") ,
    
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete") ,



]