# Generated by Django 4.0.3 on 2022-03-14 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='users',
            new_name='user',
        ),
    ]
