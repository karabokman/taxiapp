# Generated by Django 4.1 on 2022-09-06 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255, unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='Not Done', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ride_no', models.CharField(max_length=255)),
                ('driver_no', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=150)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
