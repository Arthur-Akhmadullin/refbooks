from django.db import models

class Refbook(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    code = models.CharField(max_length=100, unique=True, verbose_name='Код')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        # ordering = ['name']
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'


class Version(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    refbook_id = models.ForeignKey('Refbook',
                                   on_delete=models.CASCADE,
                                   related_name='versions',
                                   verbose_name='Наименование справочника'
                                   )
    version = models.CharField(max_length=50, verbose_name='Версия')
    date = models.DateField(verbose_name='Дата начала действия версии')

    def __str__(self):
        return self.version

    class Meta:
        ordering = ['-date']
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        unique_together = [['refbook_id', 'version'], ['refbook_id', 'date']]


class Element(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='Идентификатор')
    version_id = models.ManyToManyField('Version',
                                        through='ElementVersion',
                                        verbose_name='Версия'
                                        )
    code = models.CharField(max_length=100, unique=True, verbose_name='Код элемента')
    value = models.CharField(max_length=300, verbose_name='Значение элемента')

    def __str__(self):
        return self.value

    class Meta:
        ordering = ['value']
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'


class ElementVersion(models.Model):
    version = models.ForeignKey(Version,
                                on_delete=models.CASCADE,
                                related_name='pairs_elements',
                                verbose_name='Версия'
                                )
    element = models.ForeignKey(Element,
                                on_delete=models.CASCADE,
                                related_name='pairs_versions',
                                verbose_name='Элемент'
                                )

    class Meta:
        unique_together = ('version', 'element')
        verbose_name = ''
        verbose_name_plural = 'Элементы версий'

    def __str__(self):
        return f'Версия {self.version.version} - элемент {self.element.value} '
