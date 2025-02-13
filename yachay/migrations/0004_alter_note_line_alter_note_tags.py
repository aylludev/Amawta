# Generated by Django 5.1.4 on 2025-02-05 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yachay', '0003_remove_author_source_remove_author_type_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='line',
            field=models.ManyToManyField(blank=True, related_name='tags', to='yachay.line'),
        ),
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='notes', to='yachay.tag'),
        ),
    ]
