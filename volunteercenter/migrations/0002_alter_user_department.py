# Generated by Django 4.1 on 2022-11-09 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteercenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='department',
            field=models.CharField(choices=[('none', 'NONE'), ('delivery', 'DELIVERY'), ('prescription', 'PRESCRIPTION'), ('welfare', 'WELFARE'), ('taxi', 'TAXI')], default='none', max_length=20),
        ),
    ]