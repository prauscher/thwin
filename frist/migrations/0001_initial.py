# Generated by Django 2.2.5 on 2019-09-18 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rolle', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bezeichnung', models.CharField(max_length=50)),
                ('zeitraum', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Pruefung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eintragung', models.DateField()),
                ('ablauf', models.DateField()),
                ('frist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frist.Frist')),
            ],
        ),
        migrations.CreateModel(
            name='Fristzuordenbarkeit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frist.Frist')),
                ('rolle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rolle.Rolle')),
            ],
        ),
    ]