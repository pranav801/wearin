# Generated by Django 4.1.7 on 2023-03-22 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_remove_cartitem_user_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='is_active',
        ),
        migrations.AddField(
            model_name='cart',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
