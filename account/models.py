from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from skilldunmain.mixins import get_unique_path
from django.db.models.signals import pre_save

from django_countries.fields import CountryField

from django.urls import reverse

import hashlib
import base64
import re


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not kwargs.get('email'):
            raise ValueError('User must be needed a email address.')
        if not kwargs.get('password'):
            raise ValueError('User must be needed a password for security issue.')

        user_obj = self.model(
            email=self.normalize_email(kwargs.pop('email'))
        )

        user_obj.set_password(kwargs.pop('password'))

        for k, v in kwargs.items():
            setattr(user_obj, k, v)

        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            staff=True,
            admin=True
        )
        return user


role_choices = (
    (1, 'Administrator'),
    (2, 'Staff'),
    (3, 'Instructor'),
    (4, 'Student')
)


class User(AbstractBaseUser, PermissionsMixin):
    userid = models.SlugField(max_length=20, unique=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    pic_full_name = models.CharField(
                            max_length=30, 
                            null=True, blank=True
                        )
    email = models.EmailField(unique=True)  # core for our custom user
    first_name = models.CharField(max_length=30, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    position = models.CharField(max_length=30, null=True, blank=True)
    website = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True)
    description = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
                            upload_to='static/media/user/',
                            default="static/media/dummy-profile-pic-male.webp",
                            null=True
                        )
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    zip_postal_code = models.CharField(max_length=30, null=True)
    country = CountryField(null=True, blank=True)
    role = models.IntegerField(default=1, choices=role_choices)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    status = models.BooleanField(default=True)  # can login
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # username

    # USERNAME_FIELD and email are required by default
    REQUIRED_FIELDS = []  # ['full_name', 'email']

    def __str__(self):
        return self.email

    def get_user(self):
        return self.email

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def short_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def title_position(self):
        if self.position:
            return self.position
        elif self.title:
            return self.title

        return ""

    def full_address(self):
        return "%s\n%s, %s, %s, %s" % (
            self.address,
            self.zip_postal_code,
            self.city,
            self.country,
            self.state
        )

    def short_address(self):
        return "%s, %s, %s" % (
            self.city,
            self.country,
            self.state
        )

    def join_date(self):
        return self.create_date.date()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def role_perm(self):
        return ['', 'Admin', 'Staff', 'Instructor', 'Student'][int(self.role)]

    @property
    def status_text(self):
        return ['Inactive', 'Active'][self.status]

    @property
    def role_text(self):
        return ['', 'Admin', 'Staff', 'Instructor', 'Student'][int(self.role)]

    @property
    def is_active(self):
        return self.status

    @property
    def is_staff(self):
        return self.admin or self.staff

    @property
    def is_admin(self):
        return self.admin


def user_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.userid:
        instance.userid = get_unique_path()


pre_save.connect(user_pre_save_receiver, User)


def get_hash_path():
    path = get_unique_path()
    hash = hashlib.sha256(path.encode()).hexdigest()

    return hash


active_inactive_int = (
    (1, 'Active'),
    (2, 'Inactive')
)

class TempUserBeforeActive(models.Model):
    slug = models.SlugField(max_length=64, default=get_hash_path, unique=True)
    email = models.EmailField(unique=False)
    hash_object = models.TextField()
    is_active = models.IntegerField(choices=active_inactive_int, default=1)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.slug

    def hash_result(self):
        result = base64.b64decode(re.sub(r"b\'", '', self.hash_object))

        return result.decode()

    def get_absolute_url(self):
        return reverse('confirm_user_create', args=[self.slug])

    def save(self, *args, **kwargs):

        if self.pk is None:
            if type(self.hash_object) != str:
                self.hash_object = str(self.hash_object)

            self.hash_object = base64.b64encode(self.hash_object.encode())

        return super(TempUserBeforeActive, self).save(*args, **kwargs)


class ResetPasswordIndex(models.Model):
    reset_id = models.SlugField(max_length=64, default=get_hash_path, unique=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expire_hours = models.IntegerField(default=24)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.reset_id

    def get_absolute_url(self):
        return reverse('confirm_reset_password', args=[self.reset_id])