from django.contrib import admin

# Register your models here.
from .models import Project, Review, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Review)
admin.site.register(Tag, TagAdmin)
