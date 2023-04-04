# Generated by Django 4.1.5 on 2023-04-02 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_reviewrating'),
        ('order', '0005_alter_payment_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
