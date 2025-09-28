from django.contrib import admin


class DirectMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver')