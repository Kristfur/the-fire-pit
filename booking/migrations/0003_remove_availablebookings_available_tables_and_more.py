# Generated by Django 4.2.5 on 2023-09-25 17:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0002_alter_availablebookings_updated_by_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="availablebookings",
            name="available_tables",
        ),
        migrations.RemoveField(
            model_name="availablebookings",
            name="seats_per_table",
        ),
        migrations.RemoveField(
            model_name="booking",
            name="tables_needed",
        ),
        migrations.AddField(
            model_name="availablebookings",
            name="available_tables_large",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="availablebookings",
            name="available_tables_medium",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="availablebookings",
            name="available_tables_small",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="availablebookings",
            name="seats_per_table_large",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="availablebookings",
            name="seats_per_table_medium",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="availablebookings",
            name="seats_per_table_small",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="booking",
            name="tables_needed_large",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="booking",
            name="tables_needed_medium",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="booking",
            name="tables_needed_small",
            field=models.IntegerField(default=0),
        ),
    ]