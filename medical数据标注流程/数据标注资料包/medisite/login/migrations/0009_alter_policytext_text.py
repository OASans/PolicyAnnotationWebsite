# Generated by Django 3.2.5 on 2021-07-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_policytagger'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policytext',
            name='text',
            field=models.JSONField(null=True, verbose_name='政策原文'),
        ),
    ]
