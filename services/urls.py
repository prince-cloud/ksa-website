from unicodedata import name
from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'services'

urlpatterns = [
    ## admin page
    path("secrete-route/", views.secrete_route, name = "secrete_route"),
    path("executives/", views.executives, name = "executives"),
    path("members/", views.members, name = "members"),
    path("help-desk/ksa/", views.ksaHelpDesk, name = "ksaHelpDesk"),
    path("posts/", views.posts, name = "posts"),
    path("add-posts/", views.add_post, name = "add_post"),

    ## other pages
    path("", views.index, name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('posts/<slug:slug>/', views.postdetail, name="post-detail"),
    path('become-a-member/', views.become_a_member, name="become-a-member"),
    path('help-desk/', views.help_desk, name="helpdesk"),
    path('gallery/', views.gallery, name="gallery"),
    path('contact-us/', views.contact_us, name="contact_us"),
]