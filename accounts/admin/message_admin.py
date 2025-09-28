from django.contrib import admin


class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'content', 'timestamp')
    search_fields = ('room__name', 'sender__username', 'content')
    list_filter = ('room', 'sender')
