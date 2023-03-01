from django.contrib import admin

from .models import Refbook, Version, Element, ElementVersion
from .forms import ElementForm


class VersionInline(admin.StackedInline):
    model = Version
    fields = ['date']
    readonly_fields = ('date',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Refbook)
class RefbookAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'get_last_version', 'get_date_version']
    list_display_links = ['code', 'name']
    inlines = [VersionInline]

    def get_last_version(self, obj):
        return obj.versions.values_list('version').last()
    get_last_version.short_description = "Текущая версия"

    def get_date_version(self, obj):
        return obj.versions.values_list('date').last()
    get_date_version.short_description = "Дата начала действия"


class ElementVersionInline(admin.StackedInline):
    model = ElementVersion
    extra = 0


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['get_code_refbook', 'refbook_id', 'version', 'date']
    list_display_links = ['get_code_refbook', 'version']
    list_filter = ['refbook_id']
    inlines = [ElementVersionInline]

    def get_code_refbook(self, obj):
        return obj.refbook_id.code
    get_code_refbook.short_description = 'Код справочника'


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'value']
    list_display_links = ['code', 'value']
    list_filter = ['version_id', 'version_id__refbook_id']
    form = ElementForm
