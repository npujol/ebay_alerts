# Generated by Django 3.1.4 on 2020-12-12 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("alerts", "0002_auto_20201211_1205")]

    operations = [
        migrations.RenameField(model_name="account", old_name="id", new_name="uuid"),
        migrations.RenameField(model_name="alert", old_name="id", new_name="uuid"),
    ]
