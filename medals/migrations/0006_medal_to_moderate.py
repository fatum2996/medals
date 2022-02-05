# Generated by Django 4.0.1 on 2022-02-05 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medals', '0005_remove_profile_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medal_To_Moderate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('photo', models.ImageField(upload_to='static/images/medals/')),
                ('photo_second', models.ImageField(blank=True, upload_to='static/images/medals')),
                ('location', models.CharField(max_length=200)),
                ('org', models.CharField(blank=True, max_length=200)),
                ('added_by', models.CharField(blank=True, max_length=200)),
                ('credentials', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]