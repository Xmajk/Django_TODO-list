# Generated by Django 4.2.2 on 2023-06-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplication', '0006_alter_todo_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='todo_date',
            field=models.DateTimeField(),
        ),
    ]
