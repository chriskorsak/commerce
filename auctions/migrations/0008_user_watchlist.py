# Generated by Django 3.1.4 on 2021-01-11 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_delete_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watched', to='auctions.Listing'),
        ),
    ]
