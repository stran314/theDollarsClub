# Generated by Django 3.0.8 on 2020-07-16 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_customer_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(default='profile_default_img.png', null=True, upload_to=''),
        ),
    ]
