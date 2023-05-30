from django.contrib import admin

from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["from_user", "to_user", "edited", "readed", "sended_time"]
    list_display_links = list_display.copy()

    list_filter = ["from_user", "to_user", "edited", "readed"]

    search_fields = ["from_user", "to_user", "text_massage"]

    def has_change_permission(self, request, obj=None) -> bool:
        return False

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request) -> bool:
        return False
