from django.urls import path
from .views import (
    signup_view, login_view, logout_view,
    profile_view, profile_update_view,
    password_change_view, forgot_password_view,
    verify_reset_code_view, reset_password_view,
    change_password
)

app_name = "accounts"

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update_view, name='profile_update'),

    path('password/change/', password_change_view, name='password_change'),
    path('password/forgot/', forgot_password_view, name='forgot_password'),
    path('password/verify/', verify_reset_code_view, name='verify_reset_code'),
    path('password/reset/', reset_password_view, name='reset_password'),
    path('password/change/', change_password, name='change_password'),
]



