# Generated by Django 5.1.2 on 2025-02-06 09:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yachay', '0006_remove_note_line_remove_note_code_delete_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='author',
        ),
        migrations.AddField(
            model_name='note',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='yachay.source'),
        ),
    ]
