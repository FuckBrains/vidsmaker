# Generated by Django 3.2.4 on 2021-06-04 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto_subtitles', '0003_auto_20210601_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transcript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcript', models.TextField()),
                ('font', models.CharField(max_length=255)),
                ('text_color', models.CharField(default='#FFFFFF', max_length=7)),
                ('background_color', models.CharField(default='#000000', max_length=7)),
                ('background_opacity', models.FloatField(default=0.6)),
                ('text_size', models.IntegerField(default=20)),
            ],
        ),
        migrations.AlterField(
            model_name='document',
            name='transcript',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auto_subtitles.transcript'),
        ),
    ]
