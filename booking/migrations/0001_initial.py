# Generated by Django 4.2.5 on 2023-09-20 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("booking_name", models.CharField(max_length=25)),
                ("tables_needed", models.CharField(max_length=40)),
                ("guest_count", models.IntegerField(default=2)),
                ("booking_date", models.DateField()),
                (
                    "booking_time",
                    models.IntegerField(
                        choices=[
                            (1, "2:00pm - 3:45pm"),
                            (2, "4:00pm - 5:45pm"),
                            (3, "6:00pm - 7:45pm"),
                            (4, "8:00pm - 9:45pm"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="booking_customer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["booking_date", "booking_time"],
            },
        ),
        migrations.CreateModel(
            name="AvailableBookings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("available_tables", models.CharField(max_length=40)),
                ("seats_per_table", models.CharField(max_length=40)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                (
                    "updated_by",
                    models.ForeignKey(
                        default="empty",
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        related_name="available_bookings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
