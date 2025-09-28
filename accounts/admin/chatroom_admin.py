from django.contrib import admin


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by')
    search_fields = ('name', 'created_by__username')
