# Generated by Django 4.2.7 on 2024-01-12 15:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_alter_pofile_birthday'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Pofile',
            new_name='Profile',
        ),
    ]