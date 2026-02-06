from django.contrib import admin
from .models import Equipment, EquipmentFiles


class EquipmentFilesInline(admin.TabularInline):
    model = EquipmentFiles
    extra = 1
    fields = ('file', 'type', 'deleted')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'deleted', 'created_at')
    list_filter = ('deleted', 'created_at')
    search_fields = ('name',)
    inlines = [EquipmentFilesInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EquipmentFiles)
class EquipmentFilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment', 'type', 'deleted', 'created_at')
    list_filter = ('deleted', 'type')
    search_fields = ('equipment__name',)
    readonly_fields = ('created_at', 'updated_at', 'deleted_at')
