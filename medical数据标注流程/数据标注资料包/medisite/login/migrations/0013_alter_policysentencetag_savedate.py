# Generated by Django 3.2.5 on 2021-07-27 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0012_policytext_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policysentencetag',
            name='savedate',
            field=models.DateTimeField(auto_now=True, verbose_name='保存日期'),
        ),
    ]
