# Generated by Django 4.0 on 2022-09-09 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_alter_trip_options_rename_created_trip_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={},
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='date',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='end_address',
            new_name='drop_off_address',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='start_address',
            new_name='pick_up_address',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='is_finished',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='passenger',
        ),
        migrations.AddField(
            model_name='trip',
            name='rider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips_as_rider', to='trips.user'),
        ),
        migrations.AddField(
            model_name='trip',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='driver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='trips_as_driver', to='trips.user'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.CharField(choices=[('REQUESTED', 'REQUESTED'), ('STARTED', 'STARTED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('COMPLETED', 'COMPLETED')], default='REQUESTED', max_length=20),
        ),
    ]
