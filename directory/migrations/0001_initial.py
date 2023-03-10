# Generated by Django 3.2.17 on 2023-02-12 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код элемента')),
                ('value', models.CharField(max_length=300, verbose_name='Значение элемента')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
            },
        ),
        migrations.CreateModel(
            name='Refbook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('version', models.CharField(max_length=50, verbose_name='Версия')),
                ('date', models.DateField(verbose_name='Дата начала действия версии')),
                ('refbook_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='directory.refbook', verbose_name='Идентификтор справочника')),
            ],
            options={
                'verbose_name': 'Версия справочника',
                'verbose_name_plural': 'Версии справочников',
                'unique_together': {('version', 'date')},
            },
        ),
        migrations.CreateModel(
            name='ElementVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.element')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.version')),
            ],
            options={
                'unique_together': {('version', 'element')},
            },
        ),
        migrations.AddField(
            model_name='element',
            name='version_id',
            field=models.ManyToManyField(through='directory.ElementVersion', to='directory.Version', verbose_name='Идентификатор версии'),
        ),
    ]
