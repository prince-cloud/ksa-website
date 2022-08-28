from django.contrib import admin
from .models import Aspirant, AspirantVote, Election, Position, UserVote
# Register your models here.


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    
admin.site.register(Position)

@admin.register(Aspirant)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "picture",)
admin.site.register(UserVote)
@admin.register(AspirantVote)
class ApirantVoteAdmin(admin.ModelAdmin):
    list_display = ("user_vote", "position", "aspirant", )
    list_filter = ("position", "user_vote", "aspirant")
    
    def has_change_permission(self, *args, **kwargs) -> bool:
        return False
    