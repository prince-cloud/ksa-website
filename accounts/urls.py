from accounts.utils import generate_password
from django.http.response import Http404
from django.urls import path, include
from . import views

app_name = "accounts"


def not_found(request, *args, **kwargs):
    raise Http404("Not Found")


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    #path("dashboard/", views.dashboard, name="dashboard"),
    path("new-password/", views.get_new_password, name="get-new-password"),
]
