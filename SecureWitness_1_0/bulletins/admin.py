from django.contrib import admin
from bulletins.models import Bulletin

class BulletinAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Author', 'Date')
    list_filter = ('Date',)
    search_fields = ('Title',)

    fieldsets = [
        ('Bulletin', {
            'fields': ('Title', 'Pseudonym', 'Description')
        }),
        ('Author', {
            'classes': ('collapse',),
            'fields': ('Author',)
        }),
        ('Created At', {
            'classes': ('collapse',),
            'fields': ('Date',)
        })
    ]
    readonly_fields = ('Date',)

admin.site.register(Bulletin, BulletinAdmin)
