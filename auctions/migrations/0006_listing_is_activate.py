# Generated by Django 3.1 on 2020-12-29 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201229_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_activate',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
