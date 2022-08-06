from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.models import Group


class User(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    user_type = models.CharField(choices=(('1', 'Place Owner'),
                                          ('2', 'Costumer')), default='1', max_length=10)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        group = None
        if self.user_type == '1':
            group = Group.objects.get(name='owner')
        elif self.user_type == '2':
            group = Group.objects.get(name='costumer')
        self.groups.add(group)

    def __str__(self):
        return self.full_name
