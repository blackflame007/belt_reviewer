# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or len(postData['alias']) < 2:
            errors['name_length'] = "Name and Alias must be at least 2 characters long"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email is not valid"
        if len(postData['password']) < 8 or len(postData['confirm_password']) < 8:
            errors['pass_length'] = "Password must be 8 or more characters"
        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = "Passwords must match"
        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already taken"
        return errors
    def login(self, postData):
        errors = {}
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) > 0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = { "error": "Login Invalid" }
                return errors
        else:
            errors = { "error": "Login Invalid" }
            return errors
class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = {}
        if len(postData['review']) < 18:
            errors['review_length'] = "Length must be atleast 18 Characters..."
        if Author.objects.filter(author = postData['author']):
            errors['match'] = "Author already exist, Look at the list"
        return errors
        





class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return '<User: {} {} {} {}>'.format(self.name, self.alias, self.email, self.password)

class Author(models.Model):
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return '<Author: {}>'.format(self.author)

class Book(models.Model):
    title = models.CharField(max_length=255)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, related_name="books")
    def __repr__(self):
        return '<Book: {}>'.format(self.title)

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name="reviewer")
    books_list =models.ForeignKey(Book, related_name="book_reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()
    def __repr__(self):
        return '<Review: {} {}>'.format(self.review, self.rating)