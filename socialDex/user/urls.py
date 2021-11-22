'''URL USER'''

from django.urls import path
from . import views
app_name = 'user'

urlpatterns = [
    path("", views.login_request, name="login"),
    path("register/", views.register_request, name="register"),
    path("logout/", views.logout_request, name="logout"),
    path('users/<int:id>', views.profile, name='profile'),
    path('ip_check/', views.ip_check_view, name='ip-check-view'),
    path("password_change/", views.PasswordsChangeView.as_view(), name="password-change"),
    path("password_success/", views.password_success, name="password-success"),
]
