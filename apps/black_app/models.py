from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime
import re

now = datetime.datetime.now()


class UserManager(models.Manager):
    def validate(self, data):
        error = []
        emailreg = '[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+'
        print "Inside validate"
        if len(data['fname']) < 2 or not str.isalpha(data['fname']):
            error.append("Invalid First Name")
        if len(data['lname']) < 2 or not str.isalpha(data['lname']):
            error.append("Invalid Last Name")
        if  not re.search(emailreg, data['email']):
            error.append("Invalid Email")
        if len(data['pwd']) < 4:
            error.append("Minimum of 4 characters required for password")
        if data['pwd'] != data['conpwd']:
            error.append("Password doesn't match")
        return error

class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length= 40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class QuoteManager(models.Manager):
    def addQuote(self, quoted_by, newMsg, user):
        error = []
        if len(quoted_by) < 3:
            error.append("Too short!! Quoted BY Filed should be at least 3 characters")
        elif not quoted_by:
            error.append("This field must be filled out")  # END OF QUOTED BY VALIDATION

        if len(newMsg) < 10:
            error.append("Minimum 10 characters")  # END OF MESSAGE VALIDATION

        if len(error) > 0:
            return [False, error]
        if len(error) > 0:
            return [False, error]
        else:
            newQuote = Quotes.QuoteManager.create(message=newMsg, quoted_by=quoted_by, created_by=user.first_name,
                                                  created_at=now, updated_at=now)
            return [True]


    def validquoted_by(self, quoted_by):
        if len(quoted_by) < 3:
            return True
        else:
            return False

    def validmessage(self, newMsg):
        if len(newMsg) < 10:
            return True
        else:
            return False

class Quotes(models.Model):
    message = models.CharField(max_length=45)
    quoted_by = models.CharField(max_length=30, blank=True)
    owned_by = models.ManyToManyField(User, blank=True)
    created_by = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    QuoteManager = QuoteManager()
