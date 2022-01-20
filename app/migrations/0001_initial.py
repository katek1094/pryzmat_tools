# Generated by Django 4.0.1 on 2022-01-19 20:54

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='PlanerPhraseResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phrase', models.CharField(max_length=100)),
                ('file', models.FileField(upload_to=app.models.planer_phrase_result_path)),
            ],
        ),
        migrations.CreateModel(
            name='ScraperResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=app.models.scraper_result_path)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.account')),
            ],
        ),
    ]
