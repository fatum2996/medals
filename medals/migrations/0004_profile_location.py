# Generated by Django 4.0.1 on 2022-01-28 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medals', '0003_remove_profile_bio_remove_profile_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]