# Generated by Django 2.2.5 on 2019-09-21 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lehrgaenge', '0002_auto_20190920_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='lehrgang',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
