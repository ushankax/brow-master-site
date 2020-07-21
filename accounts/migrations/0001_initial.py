# Generated by Django 3.0.8 on 2020-07-21 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


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
                ('phone', models.CharField(max_length=255, null=True, unique=True)),
                ('bonus_points', models.IntegerField(default=0)),
                ('visits', models.IntegerField(default=0)),
            ],
        ),
    ]
