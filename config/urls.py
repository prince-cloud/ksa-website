from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('services.urls')),
    path('elections/', include('vote_app.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
