import datetime

from django.contrib import admin

from .models import Refbook, Version, Element
from .forms import ElementForm, VersionForm


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
        date_today = datetime.datetime.now()
        return obj.versions.values_list('version').filter(date__lte=date_today).\
            order_by('date').last()
    get_last_version.short_description = "Текущая версия"

    def get_date_version(self, obj):
        date_today = datetime.datetime.now()
        return obj.versions.values_list('date').filter(date__lte=date_today).\
            order_by('date').last()
    get_date_version.short_description = "Дата начала действия"


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['get_code_refbook', 'refbook_id', 'version', 'date']
    list_display_links = ['get_code_refbook', 'version']
    list_filter = ['refbook_id']
    form = VersionForm

    def get_code_refbook(self, obj):
        return obj.refbook_id.code
    get_code_refbook.short_description = 'Код справочника'

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj = Version.objects.create(refbook_id=form.cleaned_data.get('refbook_id'),
                                         version=form.cleaned_data.get('version'),
                                         date=form.cleaned_data.get('date')
                                         )
        obj.element_set.set(form.cleaned_data.get('element'))
        super().save_model(request, obj, form, change)


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'value']
    list_display_links = ['code', 'value']
    list_filter = ['version_id', 'version_id__refbook_id']
    form = ElementForm
