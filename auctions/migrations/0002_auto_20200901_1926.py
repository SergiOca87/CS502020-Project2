# Generated by Django 3.1 on 2020-09-01 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
    ]