# Generated by Django 2.2.5 on 2019-09-20 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dienst', '0003_auto_20190919_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teilnahme',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dienst_teilnahmen', to='entitaet.Person'),
        ),
    ]
