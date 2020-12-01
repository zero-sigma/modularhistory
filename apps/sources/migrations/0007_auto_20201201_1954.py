# Generated by Django 3.1.3 on 2020-12-01 19:54

import gm2m.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sources', '0006_auto_20201129_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='date_is_circa',
            field=models.BooleanField(blank=True, default=False, help_text='whether the date is estimated/imprecise', verbose_name='date is circa'),
        ),
        migrations.AlterField(
            model_name='source',
            name='related',
            field=gm2m.fields.GM2MField('quotes.Quote', 'occurrences.Occurrence', 'postulations.Postulation', blank=True, related_name='sources', through='sources.Citation', through_fields=['source', 'content_object', 'content_type', 'object_id']),
        ),
    ]
