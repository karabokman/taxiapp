# Generated by Django 4.1.1 on 2022-09-08 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passenger', '0002_hiring_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiring',
            name='passenger',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='passenger.passenger'),
        ),
    ]