# Generated by Django 3.2.5 on 2021-07-26 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20200303_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actclass',
            name='actid',
            field=models.TextField(verbose_name='文本类别'),
        ),
        migrations.AlterField(
            model_name='actclass',
            name='aid',
            field=models.TextField(verbose_name='类别id'),
        ),
    ]
