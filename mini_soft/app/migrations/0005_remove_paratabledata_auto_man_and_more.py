# Generated by Django 5.1 on 2025-01-19 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_angle_stored_delete_measurementdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paratabledata',
            name='auto_man',
        ),
        migrations.RemoveField(
            model_name='paratabledata',
            name='lsl',
        ),
        migrations.RemoveField(
            model_name='paratabledata',
            name='ltl',
        ),
        migrations.RemoveField(
            model_name='paratabledata',
            name='timer',
        ),
        migrations.RemoveField(
            model_name='paratabledata',
            name='usl',
        ),
        migrations.RemoveField(
            model_name='paratabledata',
            name='utl',
        ),
    ]
