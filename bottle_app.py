#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bottle import route, run, template, static_file, redirect, request, error
import os, sys
import codecs
import json
import psycopg2

# connect to database
conn = psycopg2.connect(dbname="db_project", host="localhost", port="5432")

def get_articles():
    pass

def save_article(title, body):
    pass

def create_slug(title):
    pass

def get_file_path_from_slug(slug):
    pass

def get_article(slug):
	pass


#Nedan listas alla rutter som i slutändan returnerar specifika templates.
@route("/")
def index():
    return template("index")

@route("/articles/create", method="GET")
def show_create_form():

    return template("articles/create")

@route("/articles", method="POST")
def store_article():
    title = request.forms.title
    body = request.forms.body

    '''
    Kontrollerar så att användaren skrivit in både titel och body,
    annars kan inte artikeln publiceras.
    '''

    if not title:
        error = "You must enter a title"
        return template("articles/create")

    if not body:
        error = "You must enter the article text"
        return template("articles/create")

    slug = create_slug(title)
    save_article(title, body)
    return (show_article(slug))

@route("/articles")
def archive():
    #Ett arkiv som visar upp alla artiklar
    return template("articles/index")

@route("/contact")
def contact():
    return template("contact")

@route('/static/<filename>')
def server_static(filename):
    # Returnerar statiska filer, t.ex. JS och CSS
    return static_file(filename, root='static')

@error(404)
def error404(error):
    return template("error")


run(host="127.0.0.1", port=8080)
