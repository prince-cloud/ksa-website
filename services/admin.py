from pickle import GLOBAL
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Member)
admin.site.register(Post)
admin.site.register(Helpdesk)
admin.site.register(Gallery)