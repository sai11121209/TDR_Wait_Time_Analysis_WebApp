# Generated by Django 3.0.7 on 2020-09-21 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standbytime', '0005_auto_20200921_1846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standbytimedatatdl',
            name='facilityCode',
            field=models.TextField(max_length=10),
        ),
        migrations.AlterField(
            model_name='standbytimedatatds',
            name='facilityCode',
            field=models.TextField(max_length=10),
        ),
    ]