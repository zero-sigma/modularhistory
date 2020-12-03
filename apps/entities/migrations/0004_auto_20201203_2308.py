# Generated by Django 3.1.4 on 2020-12-03 23:08

from django.db import migrations, models
import modularhistory.fields.array_field


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0003_auto_20201203_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='aliases',
            field=modularhistory.fields.array_field.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None, verbose_name='aliases'),
        ),
    ]
