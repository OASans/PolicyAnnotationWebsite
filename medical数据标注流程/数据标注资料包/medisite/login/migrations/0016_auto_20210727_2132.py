# Generated by Django 3.2.5 on 2021-07-27 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0015_auto_20210727_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actclass',
            name='aid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='类别id'),
        ),
        migrations.AlterField(
            model_name='labelclass',
            name='labelid',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, unique=True, verbose_name='BIO类别'),
        ),
    ]
