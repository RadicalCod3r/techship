# Generated by Django 4.0.3 on 2022-06-07 12:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('paymentMethod', models.CharField(blank=True, max_length=200, null=True)),
                ('taxPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('shippingPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('totalPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('isPaid', models.BooleanField(default=False)),
                ('paidAt', models.DateTimeField(blank=True, null=True)),
                ('isDelivered', models.BooleanField(default=False)),
                ('deliveredAt', models.DateTimeField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('address', models.CharField(blank=True, max_length=450, null=True)),
                ('city', models.CharField(blank=True, max_length=200, null=True)),
                ('postalCode', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(blank=True, max_length=200, null=True)),
                ('shippingPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shippingAddress', to='base.order')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, null=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='base.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='base.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.product')),
            ],
        ),
    ]
