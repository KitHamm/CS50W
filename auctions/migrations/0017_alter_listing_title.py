# Generated by Django 4.1 on 2022-10-30 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_bid_listing_alter_listing_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
