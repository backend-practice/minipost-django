# Generated by Django 2.2.5 on 2019-09-03 05:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nickname', models.CharField(blank=True, max_length=64, unique=True)),
                ('gender', models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'Male'), (2, 'Female')], default=0)),
                ('avatar', models.ImageField(blank=True, upload_to=users.models.avatar_image_path)),
            ],
        ),
    ]
