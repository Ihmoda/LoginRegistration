# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
import re
# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "Users must submit a name"
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Users must submit a last name"
        if len(postData['email']) < 1:
            errors['email'] = "Users must submit an email"
        if len(postData['password']) < 1:
            errors['password'] = "Users must submit a password"
        if len(postData['confirm_password']) < 1:
            errors['confirm_password'] = "Users must confirm password"

        if len(errors) > 0:
            return errors

        birthday_date = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')

        if birthday_date > datetime.datetime.now():
            errors['birthday'] = "Birthday must be prior to today's date."
  

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.-]+\@[a-zA-Z0-9_.-]+\.[a-zA-Z0-9_.-]{2,4}$')
        NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')
        PASSWORD_REGEX = re.compile(r'^.{8,}$')

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Users must submit a valid email"
        
        if not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First name can only contain letters and must be at least two characters."
        
        if not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last name can only contain letters and must be at least two characters."
        
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Password must contain at least eight characters"
        
        if not postData['password'] == postData['confirm_password']:
            errors['password'] = "Passwords must match"


        # check if email exists in the database
        result = User.objects.filter(email=postData['email'])

        if len(result) > 0:
            errors['emailexists'] = "Email already registered to user."

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField(default=None)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateField(auto_now_add= True)

    objects = UserManager()

