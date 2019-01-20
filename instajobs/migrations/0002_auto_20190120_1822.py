# Generated by Django 2.1.5 on 2019-01-20 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instajobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='external_id',
            field=models.SlugField(blank=True, editable=False, max_length=150),
        ),
        migrations.AddField(
            model_name='job',
            name='sender',
            field=models.SlugField(blank=True, default='instajobs', editable=False, max_length=150),
        ),
    ]
