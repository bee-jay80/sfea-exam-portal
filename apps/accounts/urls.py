from django.urls import path

from .views import CurrentUserView, LoginView, RegisterView, UserListView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("login/", LoginView.as_view(), name="auth_login"),
    path("me/", CurrentUserView.as_view(), name="auth_me"),
    path("users/", UserListView.as_view(), name="user_list"),
]
