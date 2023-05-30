from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from rest_framework.authtoken.models import (
    TokenProxy as RestFrameworkTokenProxy,
)

from evants.models import Evants

from .models import (
    FAQ,
    Comment,
    Contact,
    Doctor,
    Opinion,
    Professions,
    Token,
    User,
)

admin.site.unregister(RestFrameworkTokenProxy)


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = [
        "user_info",
        "user_ip",
        "created",
        "country",
        "timezone",
        "browser",
        "device",
        "os",
        "is_active",
        "get_device_type",
    ]
    list_display_links = list_display.copy()
    readonly_fields = ["created", "get_device_type", "get_user_ip"]
    list_filter = [
        "country",
        "region",
        "timezone",
        "browser",
        "device",
        "os",
        "deleted",
    ]
    date_hierarchy = "created"
    icons = {
        "is_bot": ["#007bff", "fas fa-robot"],
        "is_email_client": ["#6f42c1", "fas fa-at"],
        "is_mobile": ["#fd7e14", "fas fa-mobile-alt"],
        "is_pc": ["#28a745", "fas fa-desktop"],
        "is_tablet": ["#e83e8c", "fas fa-tablet-alt"],
        "is_touch_capable": ["red", "fas fa-fingerprint"],
    }
    exclude = ["user_ip", *list(icons.keys()).copy()]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def user_info(self, obj=None):
        return f"{obj.user.email if obj.user else 'Unknown'}"

    user_info.short_description = "User"  # type: ignore
    user_info.admin_order_field = "user__id"  # type: ignore

    def get_device_type(self, obj):
        fields = [
            f"<i title=\"{k.title().replace('_', ' ')}\" style=\"color:{v[0]}\" class=\"{v[1]}\"></i>"  # noqa
            for k, v in self.icons.items()
            if (getattr(obj, k))
        ]
        fields = (
            [
                '<i title="Other" style="color:{v[0]}" class="{v[1]}"></i>'.format(  # noqa
                    v=["yellow", "fas fa-question"]
                )
            ]
            if len(fields) == 0
            else fields
        )
        return mark_safe("&nbsp;&nbsp;&nbsp;&nbsp;".join(fields))

    get_device_type.short_description = "Device type"  # type: ignore

    def get_user_ip(self, obj=None):
        return (
            mark_safe(
                '<a href="https://ipinfo.io/{0}/json" target="_blank">{0}</a>'.format(  # noqa
                    obj.user_ip
                )
            )
            if obj.user_ip
            else "-"
        )  # noqa

    get_user_ip.short_description = "IP"  # type: ignore

    def is_active(self, obj=None):
        return not obj.deleted

    is_active.boolean = True  # type: ignore
    is_active.admin_order_field = "-deleted"  # type: ignore


@admin.register(Professions)
class ProfessionsAdmin(TranslationAdmin):
    pass


@admin.register(Opinion)
class OpinionAdmin(TranslationAdmin):
    pass


@admin.register(Doctor)
class DoctorAdmin(TranslationAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Evants)
class EvantsAdmin(admin.ModelAdmin):
    pass


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    pass
