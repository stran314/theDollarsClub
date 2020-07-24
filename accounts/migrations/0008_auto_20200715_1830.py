# Generated by Django 3.0.8 on 2020-07-15 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_customer_membership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='membership',
            field=models.CharField(choices=[('Non-Member', 'Non-Member'), ('Bronze', 'Bronze'), ('Silver', 'Silver'), ('Platinum', 'Platinum'), ('Diamond', 'Diamond'), ('Dollars', 'Dollars')], default='Non-Member', max_length=200, null=True),
        ),
    ]
