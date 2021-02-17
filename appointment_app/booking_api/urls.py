from django.urls import path
from booking_api import views

urlpatterns = [
    path("",views.index,name="index"),
    path("appointment/book",views.book,name="book"),
    path("appointment/book/confirm",views.confirm,name="confirm"),
    path("appointments/<pk>/",views.update_appointment,name="update_appointment"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("dashboard/completed_appointments/",views.completed_appointments,name="completed_appointments"),
    path("login/",views.user_login,name="login"),
]