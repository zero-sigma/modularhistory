# Generated by Django 3.0.4 on 2020-04-04 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0026_auto_20200404_0137'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='edition_year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
