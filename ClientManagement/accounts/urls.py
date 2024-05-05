from django.urls import path
from . import views

urlpatterns = [
     path("register/", views.register, name="register"),
     path("login/", views.login, name="login"),
     path('logout/', views.logout, name='logout'),
     path("reset-password-verify-email/", views.reset_password_verify_email, name="verify_email"),
     path('reset-password-otp/', views.reset_password_verify_otp, name="verify_otp"),
     path("employees/view", views.view_employees, name="view_employees"),
     path("employees/delete/confirm/<int:employee_id>/", views.delete_employee_confirm, name="delete_employee_confirm"),
     path("employee/delete/confirmed/<int:employee_id>/", views.delete_employee, name="delete_employee"),
     path("employee/reverse_status/confirm/<int:employee_id>/", views.reverse_employee_status_confirm, name="reverse_employee_status_confirm"),
     path("employee/reverse_status/<int:employee_id>/", views.reverse_employee_status, name="reverse_employee_status"),
]
