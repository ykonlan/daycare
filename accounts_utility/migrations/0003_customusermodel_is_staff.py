# Generated by Django 5.2.1 on 2025-05-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts_utility', '0002_remove_customusermodel_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
