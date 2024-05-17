# Generated by Django 4.2.7 on 2024-05-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_rename_site_fonte_sources_web_source_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedtext',
            name='Fontes',
            field=models.ManyToManyField(to='App.sources'),
        ),
        migrations.AlterField(
            model_name='checkedfile',
            name='arquivo',
            field=models.FileField(blank=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='uploadedtext',
            name='texto',
            field=models.TextField(default='Insira o texto que deseja verificar.', max_length=1000),
        ),
    ]