# Generated by Django 3.2.3 on 2021-05-20 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorteo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_verify',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date verify'),
        ),
    ]
