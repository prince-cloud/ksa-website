from django.urls import path
from .import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'services'

urlpatterns = [
    ## admin page
    path("secrete-route/", views.secrete_route, name = "secrete_route"),
    path("executives/", views.executives, name = "executives"),
    path("add-executive/", views.add_executive, name = "add_executive"),
    path("members/", views.members, name = "members"),
    path("help-desk/ksa/", views.ksaHelpDesk, name = "ksaHelpDesk"),
    path("posts/", views.posts, name = "posts"),
    path("add-posts/", views.add_post, name = "add_post"),
    path("add-yeargroup/", views.add_yeargroup, name = "add_yeargroup"),
    path("add-position/", views.add_position, name = "add_position"),
    path("admin-gallery/", views.admin_gallery, name = "admin_gallery"),
    path("upload-images/", views.upload_gallery_images, name = "upload_gallery_images"),
    path("delete-gallery-image/<int:id>/", views.delete_gallery_image, name = "delete_gallery_image"),
    path("delete-event/<int:id>/", views.delete_event, name = "delete_event"),
    path("events/", views.events, name = "events"),
    path("add-event/", views.add_event, name = "add_event"),

    ## other pages
    path("", views.index, name="index"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('posts/<slug:slug>/', views.postdetail, name="post-detail"),
    path('all-post/', views.all_post, name="all-post"),
    path('delete-post/<int:id>/', views.delete_post, name="delete-post"),
    path('become-a-member/', views.become_a_member, name="become-a-member"),
    path('help-desk/', views.help_desk, name="helpdesk"),
    path('gallery/', views.gallery, name="gallery"),
    path('contact-us/', views.contact_us, name="contact_us"),
]