# Generated by Django 4.0 on 2022-09-11 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0008_alter_trip_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]