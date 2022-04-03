from unicodedata import name
from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'services'

urlpatterns = [
    path("", views.index, name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('posts/<slug:slug>/', views.postdetail, name="post-detail"),
    path('become-a-member/', views.become_a_member, name="become-a-member"),
    path('help-desk/', views.help_desk, name="helpdesk"),
]