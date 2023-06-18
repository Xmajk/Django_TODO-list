from django.urls import path
from . import views

urlpatterns=[
    path("home/",views.index,name="home_index"),
    path("control/",views.control_page,name="control"),
    path("login/",views.login_page,name="login"),
    path("logout/",views.logout_path,name="logout"),
    path("home/api/delete_todo",views.delete_todo,name="home_api_create_todo"),
    path("home/api/change_todo",views.change_todo,name="home_api_change_todo"),
    path("home/api/get_status",views.get_not_done,name="home_api_get_status")
]