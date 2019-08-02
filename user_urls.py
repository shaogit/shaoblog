from django.urls import path

from main.user import views

urlpatterns = [
    path("login",views.LoginView.as_view(),name="main.login"),
    path("logout",views.LoginView.as_view(),name="main.logout"),
    path("register",views.RegisterView.as_view(),name="main.register"),

    path("password/reset", views.PasswordResetView.as_view(), name="main.password.reset"),
    path("password/reset/confirm/<uidb64>/<token>", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password/reset/done',views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('password/reset/complete',views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
]
