# Generated by Django 4.0.6 on 2022-08-07 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[(None, '----'), ('1', 'Place Owner'), ('2', 'Costumer')], default='0', max_length=10),
        ),
    ]
