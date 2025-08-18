from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.login_page_render.as_view(),name="login"),
    path("dashboard/",views.dashboard_render.as_view(),name="dashboard"),
    path("logout/",views.logout_view.as_view(),name="logout"),
]