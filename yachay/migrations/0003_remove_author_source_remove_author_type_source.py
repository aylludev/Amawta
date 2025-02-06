# Generated by Django 5.1.4 on 2025-02-05 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yachay', '0002_remove_note_line_alter_note_tags_note_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='source',
        ),
        migrations.RemoveField(
            model_name='author',
            name='type',
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('type', models.CharField(choices=[('BOOK', 'Book'), ('ESSAY', 'Essay'), ('ARTICLE', 'Article'), ('VIDEO', 'Video'), ('OTHER', 'Other')], default='OTHER', max_length=10)),
                ('author', models.ManyToManyField(blank=True, related_name='author', to='yachay.author')),
            ],
        ),
    ]
