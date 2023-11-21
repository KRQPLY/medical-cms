# Generated by Django 3.2.6 on 2023-11-21 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0010_auto_20231120_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature',
            name='page',
        ),
        migrations.AddField(
            model_name='feature',
            name='page',
            field=models.ManyToManyField(blank=True, to='client.Page'),
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='page',
        ),
        migrations.AddField(
            model_name='schedule',
            name='page',
            field=models.ManyToManyField(blank=True, to='client.Page'),
        ),
        migrations.RemoveField(
            model_name='slider',
            name='page',
        ),
        migrations.AddField(
            model_name='slider',
            name='page',
            field=models.ManyToManyField(blank=True, to='client.Page'),
        ),
    ]