# Generated by Django 3.2.5 on 2021-07-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_alter_policysentencetag_savedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actclass',
            name='aid',
            field=models.IntegerField(verbose_name='类别id'),
        ),
    ]
