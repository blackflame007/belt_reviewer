# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from models import *
from django.contrib import messages
import bcrypt
from django.contrib.sessions.models import Session

def index(request):
    return render(request, "book_reviews/index.html")

def process(request):
    print request.POST
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw)
        request.session['id'] = user.id
        messages.success(request, "You have successfully registered")
    return redirect('/books')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/books')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def logout(request):
    Session.objects.all().delete()
    return redirect('/')

def books(request):
    if not 'id' in request.session:
        return redirect ('/')
    context = {
        'user': User.objects.get(id=request.session['id']),
        'reviews': Review.objects.all().order_by("-created_at")
    }
    return render(request, "book_reviews/books.html", context)

def create_review(request):
    if not 'id' in request.session:
        return redirect ('/')
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'book_reviews/add_book.html', context)

def new_review(request):
    if not 'id' in request.session:
        return redirect ('/')
    errors = Review.objects.review_validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/create_review')
    else:
        if len(request.POST['author']) > 0:
            new_author = Author.objects.create(author = request.POST['author'])
            new_book = Book.objects.create(title=request.POST['title'], author = new_author)
        else:
            new_book = Book.objects.create(title=request.POST['title'], author= Author.objects.get(id = request.POST['authors']))
        new_review = Review.objects.create(review=request.POST['review'], rating = request.POST['rating'], user = User.objects.get(id = request.session['id']), books_list = new_book)
        return redirect('/books')

def book_reviews(request, book_id):
    if not 'id' in request.session:
        return redirect ('/')
    context ={
        'book': Book.objects.get(id=book_id),
        'reviews': Review.objects.filter(books_list__id=book_id)
    }
    return render(request, "book_reviews/book_reviews.html", context)


def add_review(request, book_id):
    if not 'id' in request.session:
        return redirect ('/')
    curr_book = Book.objects.get(id=book_id) #.filter( author = Author.objects.filter(books__id = book_id))
    new_review = Review.objects.create(review=request.POST['review'], rating = request.POST['rating'], user = User.objects.get(id = request.session['id']), books_list = curr_book)
    return redirect('/books/{}'.format(book_id))

    
def user(request, user_id):
    if not 'id' in request.session:
        return redirect ('/')
    context = {
        'user': User.objects.get(id=user_id),
        'reviews': Review.objects.filter(user=user_id)
    }
    return render(request, "book_reviews/users.html", context)