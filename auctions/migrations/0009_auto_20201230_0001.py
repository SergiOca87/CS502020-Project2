# Generated by Django 3.1 on 2020-12-29 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_won_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='is_activate',
            new_name='is_active',
        ),
    ]
