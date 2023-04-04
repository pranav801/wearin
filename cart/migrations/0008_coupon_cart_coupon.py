# Generated by Django 4.1.7 on 2023-03-27 02:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_cart_razorpay_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=20)),
                ('discount_price', models.PositiveIntegerField(default=799)),
                ('min_amount', models.PositiveIntegerField(default=17999)),
                ('is_expired', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.coupon'),
        ),
    ]
