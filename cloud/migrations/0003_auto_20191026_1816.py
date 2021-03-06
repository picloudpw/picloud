# Generated by Django 2.0.2 on 2019-10-26 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0002_remove_userinfo_vk_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256)),
                ('short_name', models.CharField(blank=True, max_length=64, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, default='resources/default/department.png', null=True, upload_to='resources/logo/')),
                ('is_approved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HierarchyLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.HierarchyLevel'),
        ),
        migrations.AddField(
            model_name='hierarchy',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Hierarchy'),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='hierarchy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Hierarchy'),
        ),
        migrations.AddField(
            model_name='memesource',
            name='hierarchy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Hierarchy'),
        ),
        migrations.AddField(
            model_name='subject',
            name='hierarchy',
            field=models.ManyToManyField(to='cloud.Hierarchy'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='hierarchy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cloud.Hierarchy'),
        ),
    ]
