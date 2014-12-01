from django.contrib import admin
from bulletins.models import Bulletin, File

class FilesInline(admin.TabularInline):
    model = File
    extra = 1

class BulletinAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Author', 'Date')
    list_filter = ('Date',)
    search_fields = ('Title',)

    fieldsets = [
        ('Bulletin', {
            'fields': ('Title', 'Pseudonym', 'Location', 'Description')
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
    inlines = [FilesInline]
    readonly_fields = ('Date', 'Title', 'Pseudonym', 'Location', 'Description')

admin.site.register(Bulletin, BulletinAdmin)
