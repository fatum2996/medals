# Generated by Django 4.0.1 on 2022-01-09 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medals', '0007_series_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='logo',
            field=models.FileField(blank=True, upload_to='static/images/logos/series'),
        ),
    ]
