# Generated by Django 4.0.3 on 2022-06-26 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_orderitem_image_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='images/sample.jpg', null=True, upload_to='images/'),
        ),
    ]
