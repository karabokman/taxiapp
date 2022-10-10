# Generated by Django 4.1 on 2022-09-06 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('driver', '0003_alter_driver_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='name',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='surname',
        ),
        migrations.AlterField(
            model_name='driver',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]