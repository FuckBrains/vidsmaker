# Generated by Django 3.2.4 on 2021-06-14 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_subtitles', '0006_document_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]