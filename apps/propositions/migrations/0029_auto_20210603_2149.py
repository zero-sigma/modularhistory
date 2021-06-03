# Generated by Django 3.1.11 on 2021-06-03 21:49

from django.db import migrations


def convert_data(apps, schema_editor):
    Model = apps.get_model('propositions', 'PolymorphicProposition')
    Model.objects.filter(type='propositions.proposition').update(
        type='propositions.conclusion'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('propositions', '0028_auto_20210603_0548'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Proposition',
        ),
        migrations.CreateModel(
            name='Conclusion',
            fields=[],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('propositions.polymorphicproposition',),
        ),
        migrations.RunPython(convert_data, migrations.RunPython.noop),
    ]
