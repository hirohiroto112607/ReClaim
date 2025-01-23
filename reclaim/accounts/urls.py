from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('logout_get/', views.logout_get, name="logout_get"),
    path('profile/', views.profile, name="profile"),
    path('profile_edit/', views.ProfileEditView.as_view(), name="edit_profile"),
    path('password_change/', views.PasswordChange.as_view(),
         name='password_change'),

]
