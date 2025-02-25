# Generated by Django 5.1.4 on 2025-02-23 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0017_returningtransaction"),
    ]

    operations = [
        migrations.AddField(
            model_name="returningtransaction",
            name="late_return_penalty",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
