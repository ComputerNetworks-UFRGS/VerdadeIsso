# Generated by Django 4.2.7 on 2024-05-16 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0013_uploadedtext_fontes_alter_checkedfile_arquivo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckedText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default='Insira o texto que deseja verificar.', max_length=1000)),
                ('hash_value', models.CharField(blank=True, max_length=64)),
                ('fake', models.BooleanField(default=False)),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
