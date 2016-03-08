from django.contrib import admin

from eventualgram.models import InstagramMedia


class InstagramMediaAdmin(admin.ModelAdmin):
    list_display = ('instagram_id', 'username', 'created_time', 'url')


admin.site.register(InstagramMedia, InstagramMediaAdmin)
