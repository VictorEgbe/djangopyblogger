from django.urls import path

from .views import (
    UserResetView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
    UserPasswordResetCompleteView
)
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.registration, name='register'),
    path('password_change/', views.password_change, name='password_change'),
    path('password_reset/', UserResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/done/', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete')
]
