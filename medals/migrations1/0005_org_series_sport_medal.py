# Generated by Django 4.0.1 on 2022-01-09 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medals', '0004_alter_city_region'),
    ]

    operations = [
        migrations.CreateModel(
            name='Org',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('count', models.IntegerField(default=0)),
                ('descriprion', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('logo', models.ImageField(blank=True, upload_to='static/images/logos/orgs')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('count', models.IntegerField(default=0)),
                ('descriprion', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, upload_to='static/images/logos/series')),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('count', models.IntegerField(default=0)),
                ('descriprion', models.TextField(blank=True)),
                ('logo', models.ImageField(blank=True, upload_to='static/images/logos/sports')),
            ],
        ),
        migrations.CreateModel(
            name='Medal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date_added', models.DateField(auto_now=True)),
                ('date', models.DateField(auto_now=True)),
                ('distance', models.CharField(blank=True, max_length=15)),
                ('photo', models.ImageField(upload_to='static/images/medals/')),
                ('photo_second', models.ImageField(blank=True, upload_to='static/images/medals')),
                ('likes', models.IntegerField(default=0)),
                ('added_by', models.CharField(blank=True, max_length=200)),
                ('credentials', models.CharField(blank=True, max_length=200)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medals.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medals.country')),
                ('org', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medals.org')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medals.region')),
                ('series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='medals.series')),
                ('sport', models.ForeignKey(default='Бег', on_delete=django.db.models.deletion.CASCADE, to='medals.sport', to_field='name')),
            ],
        ),
    ]
