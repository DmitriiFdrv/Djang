
from django.db import models
from django.contrib.auth.models import User, AbstractUser
import pytz
from django.conf import settings
from datetime import datetime, timedelta


class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    avatar = models.ImageField(upload_to='users_avatars', blank=True)

    activation_key = models.CharField(max_length=128, verbose_name='ключ активации', blank=True, null=True)
    activation_key_expires = models.DateTimeField(blank=True, null=True)

    def is_activate_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activate_key_expired + timedelta(hours=48):
            return True
        return False
