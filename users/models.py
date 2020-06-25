from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete = models.CASCADE)
    college = models.CharField(default='', max_length=100, verbose_name='College Name')
    year = models.CharField(default='', max_length=30, verbose_name='Year')
    branch = models.CharField(default='', max_length=30, verbose_name='Branch')
    id_proof = models.CharField(default='', max_length=30, verbose_name='ID Proof')

    def __str__(self):
        return f'{ self.user.username } Profile'