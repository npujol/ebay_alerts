# Generated by Django 3.1.4 on 2020-12-14 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("alerts", "0003_auto_20201212_1255")]

    operations = [
        migrations.AlterUniqueTogether(
            name="alert", unique_together={("search_term", "interval_time", "owner")}
        )
    ]
