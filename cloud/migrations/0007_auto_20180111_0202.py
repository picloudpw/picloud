# Generated by Django 2.0.1 on 2018-01-10 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0006_auto_20180111_0154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='program',
            name='start_year',
        ),
        migrations.AddField(
            model_name='program',
            name='code',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]