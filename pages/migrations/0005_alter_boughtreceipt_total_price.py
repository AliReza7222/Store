# Generated by Django 4.1.1 on 2023-07-17 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_boughtreceipt_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boughtreceipt',
            name='total_price',
            field=models.CharField(editable=False, max_length=15),
        ),
    ]
