# Generated by Django 4.1.5 on 2023-04-03 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_home', '0005_alter_user_address_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_address',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
