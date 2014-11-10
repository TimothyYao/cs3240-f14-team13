from django.contrib import admin

from stories.models import Story

class StoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'domain', 'author', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'author__username')

    def lower_case_title(self, obj):
        return obj.title.lower()
    lower_case_title.short_description = 'title'

admin.site.register(Story)
# Register your models here.
