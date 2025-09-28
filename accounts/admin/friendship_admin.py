from django.contrib import admin


class FriendShipAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'status')