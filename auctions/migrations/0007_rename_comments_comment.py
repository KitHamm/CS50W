# Generated by Django 4.1 on 2022-10-30 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_comments'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='comments',
            new_name='comment',
        ),
    ]