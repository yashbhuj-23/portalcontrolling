# Generated by Django 5.2.1 on 2025-06-23 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_resumerequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resumerequest',
            old_name='name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='resumerequest',
            old_name='user',
            new_name='user_id',
        ),
    ]
