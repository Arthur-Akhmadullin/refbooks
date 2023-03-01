from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Version, Element


class VersionsMultipleModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s -> %s" % (obj.refbook_id, obj.version)


class ElementForm(forms.ModelForm):
    version_id = VersionsMultipleModelChoiceField(queryset=(Version.objects.all().
                                                            order_by('refbook_id', '-version')),
                                                  label=('Справочники | Версии'),
                                                  required=False,
                                                  widget=FilteredSelectMultiple(
                                                      verbose_name=('справочники -> версии'),
                                                      is_stacked=False
                                                  ),
                                                  )

    def __init__(self, *args, **kwargs):
        super(ElementForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['version_id'].initial = self.instance.version_id.all()

    class Meta:
        model = Element
        fields = ['code', 'value']


class VersionForm(forms.ModelForm):
    element = forms.ModelMultipleChoiceField(queryset=(Element.objects.all().order_by('value')),
                                             label=('Элементы справочников'),
                                             required=False,
                                             widget=FilteredSelectMultiple(
                                                 verbose_name=('элементы справочников'),
                                                 is_stacked=False
                                             ),
                                             )

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['element'].initial = self.instance.element_set.all()

    class Meta:
        model = Version
        fields = ['refbook_id', 'version', 'date']
