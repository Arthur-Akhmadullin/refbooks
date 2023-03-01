from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Version, Element


class VersionsMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s -> %s" % (obj.refbook_id, obj.version)


class ElementForm(forms.ModelForm):
    version_id = VersionsMultipleModelChoiceField(queryset=(Version.objects.all()),
                                                  label=('Справочники | Версии'),
                                                  required=False,
                                                  widget=FilteredSelectMultiple(
                                                      verbose_name=('справочники -> версии'),
                                                      is_stacked=False
                                                  ),
                                                  )

    def __init__(self, *args, **kwargs):
        super(ElementForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['version_id'].initial = self.instance.version_id.all()

    class Meta:
        model = Element
        fields = ['code', 'value']
