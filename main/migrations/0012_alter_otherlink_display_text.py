# Generated by Django 5.0.4 on 2024-05-09 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_userdata_image_alter_userdata_nin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherlink',
            name='display_text',
            field=models.CharField(max_length=35),
        ),
    ]
