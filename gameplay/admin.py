from django.contrib import admin
from .models import Game, Move


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    Model GameAdmin class receive attribute list_display for display's settings configurations for admin interface.
    """
    list_display = ('id', 'first_player', 'second_player', 'status')
    list_editable = ('status',)


admin.site.register(Move)

