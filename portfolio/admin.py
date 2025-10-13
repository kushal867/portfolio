from django.contrib import admin
from .models import Project, Skill

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    search_fields = ('title', 'description')
    list_filter = ('title',)
    ordering = ('title',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name',)
    list_filter = ('level',)
    ordering = ('name',)
