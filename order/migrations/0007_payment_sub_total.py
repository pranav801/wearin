# Generated by Django 4.1.5 on 2023-04-02 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_orderitem_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='sub_total',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
