# Generated by Django 2.1.5 on 2019-01-08 19:30

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Name')),
                ('var_name', models.SlugField(max_length=32, unique=True, verbose_name='Slug')),
                ('title', models.TextField(blank=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('keywords', models.TextField(blank=True, verbose_name='Keywords')),
                ('category_order', models.PositiveIntegerField(blank=True, unique=True, verbose_name='Category order')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Name')),
                ('ascii_name', models.SlugField(unique=True, verbose_name='ASCII Name')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('description_html', models.TextField(editable=False)),
                ('company', models.CharField(max_length=150, verbose_name='Company')),
                ('company_slug', models.SlugField(editable=False, max_length=150)),
                ('outside_location', models.CharField(blank=True, max_length=150, verbose_name='Outside location')),
                ('url', models.URLField(blank=True, max_length=150)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created on')),
                ('status', models.IntegerField(choices=[(0, 'Inactive'), (1, 'Temporary'), (2, 'Active')], default=1)),
                ('views_count', models.IntegerField(default=0, editable=False)),
                ('auth', models.CharField(blank=True, editable=False, max_length=32)),
                ('joburl', models.CharField(blank=True, editable=False, max_length=32)),
                ('poster_email', models.EmailField(help_text='Applications will be sent to this address.', max_length=254, verbose_name='Poster email')),
                ('apply_online', models.BooleanField(default=True, help_text='If you are unchecking this, then add a description on how to apply online!', verbose_name='Allow online applications.')),
                ('spotlight', models.BooleanField(default=False, verbose_name='Spotlight')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djobberbase.Category', verbose_name='Category')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='djobberbase.City', verbose_name='City')),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
            },
        ),
        migrations.CreateModel(
            name='JobSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=100, verbose_name='Keywords')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on')),
            ],
            options={
                'verbose_name': 'Search',
                'verbose_name_plural': 'Searches',
            },
        ),
        migrations.CreateModel(
            name='JobStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.GenericIPAddressField()),
                ('stat_type', models.CharField(choices=[('A', 'Application'), ('H', 'Hit'), ('S', 'Spam')], max_length=1)),
                ('description', models.CharField(max_length=250, verbose_name='Description')),
                ('job', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djobberbase.Job')),
            ],
            options={
                'verbose_name': 'Job Stat',
                'verbose_name_plural': 'Job Stats',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='Name')),
                ('var_name', models.SlugField(max_length=32, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
            },
        ),
        migrations.AddField(
            model_name='job',
            name='jobtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='djobberbase.Type', verbose_name='Job Type'),
        ),
    ]
