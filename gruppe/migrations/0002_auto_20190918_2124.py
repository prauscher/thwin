# Generated by Django 2.2.5 on 2019-09-18 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gruppe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gruppe',
            name='uebergeordnet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gruppe.Gruppe'),
        ),
    ]
