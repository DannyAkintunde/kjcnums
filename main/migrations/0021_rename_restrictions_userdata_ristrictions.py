# Generated by Django 5.0.4 on 2024-05-10 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_alter_nin_nin_alter_nin_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdata',
            old_name='restrictions',
            new_name='ristrictions',
        ),
    ]
