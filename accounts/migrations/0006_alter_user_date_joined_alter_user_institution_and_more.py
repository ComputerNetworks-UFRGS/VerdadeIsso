# Generated by Django 4.2.7 on 2024-05-17 14:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_options_remove_user_job_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='user',
            name='institution',
            field=models.CharField(blank=True, max_length=100, verbose_name='Instituição'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, max_length=100, verbose_name='Papel'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='A username that will be used for identification and login on the platform.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(code='invalid', message='Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.', regex='^[\\w.@+-]+$')], verbose_name='Usuário'),
        ),
    ]