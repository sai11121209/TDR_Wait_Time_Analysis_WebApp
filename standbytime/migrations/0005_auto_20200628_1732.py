# Generated by Django 3.0.7 on 2020-06-28 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("standbytime", "0004_auto_20200628_0044"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standbytimedata",
            name="facility_fastpass_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="standbytimedata",
            name="facility_fastpass_start",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="standbytimedata",
            name="operating_status_end",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="standbytimedata",
            name="operating_status_start",
            field=models.DateTimeField(null=True),
        ),
    ]
