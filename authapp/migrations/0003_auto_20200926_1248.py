# Generated by Django 2.2 on 2020-09-26 09:48

import authapp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20200831_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tagline', models.CharField(blank=True, max_length=128, verbose_name='теги')),
                ('aboutMe', models.TextField(blank=True, max_length=512, verbose_name='о себе')),
                ('gender', models.CharField(blank=True, choices=[('M', 'мужской'), ('W', 'женский')], max_length=1, verbose_name='пол')),
            ],
        ),
        migrations.AlterModelOptions(
            name='shopuser',
            options={'ordering': ['-is_active', '-is_superuser', '-is_staff', 'username']},
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=authapp.models.get_activation_key_expires),
        ),
    ]
