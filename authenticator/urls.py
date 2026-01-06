
from django.urls import path, include
from .views import LoginView, LogoutView, RegisterUserView, GetUserView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path("<uuid:student_id>/", GetUserView.as_view(), name="get-user"),
]