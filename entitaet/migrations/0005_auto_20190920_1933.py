# Generated by Django 2.2.5 on 2019-09-20 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entitaet', '0004_auto_20190920_1650'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='authCode',
            new_name='auth_code',
        ),
    ]
