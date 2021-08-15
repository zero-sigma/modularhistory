# Generated by Django 3.1.12 on 2021-06-10 18:10

import django.db.models.deletion
from django.db import migrations

import core.fields.m2m_foreign_key


class Migration(migrations.Migration):

    dependencies = [
        ('collections', '0001_initial'),
        ('entities', '0005_auto_20210610_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectioninclusion',
            name='collection',
            field=core.fields.m2m_foreign_key.ManyToManyForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='entities_collectioninclusion_set',
                to='collections.collection',
            ),
        ),
    ]
