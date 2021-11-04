from django.contrib import admin
from .models import UserInfo


class UserAdmin(admin.ModelAdmin):
    list_display = ["user", "ip_address", "last_login"]

    class Meta:
        model = UserInfo


# Register your models here.
admin.site.register(UserInfo, UserAdmin)