# Generated by Django 3.2.5 on 2021-07-27 10:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_policysentence_policysentencetag_policytext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='policysentencetag',
            old_name='dialogue_act',
            new_name='sentence_tag',
        ),
        migrations.AddField(
            model_name='policysentencetag',
            name='reviewer',
            field=models.IntegerField(default=0, verbose_name='用户id'),
        ),
        migrations.AddField(
            model_name='policysentencetag',
            name='savedate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期'),
        ),
    ]
