#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, template, static_file, redirect, request, error
import os, sys
import codecs
import json

def get_articles():
    # Listar alla filer som finns i storage
    files = os.listdir("storage")

    # Filtrerar filerna så att inte dolda filer skrivs ut, ex .DS_Store
    filtered_files = [file for file in files if not file.startswith('.')]
    articles = []

    for file in filtered_files:
        slug, extension = os.path.splitext(file)
        # Läser in varje fil i en dictionary
        article = get_article(slug)
        articles.append(article)

    # Returnerar resultatet som en lista av flera dicitionarys
    return articles

def save_article(title, body):
    # Skapar en slug från titeln för en snyggare utskrift i url:n
    slug = create_slug(title)

    # Hämtar en specifik sökväg
    file_name = get_file_path_from_slug(slug)

    '''
    Öppnar filen i skrivläge och skriver innehållet i en jsonfil i följande
    ordning. Stänger därefter filen.
    '''
    file = codecs.open(file_name, "w", 'UTF-8')
    file.write(json.dumps({
        "title": title,
        "body": body,
        "slug": slug,
    }))
    file.close()

def create_slug(title):
    #För en snyggare utskrift i URL:n byter jag ut åäö samt mellanslag mot "a" "o" och "-".
    return title.lower().replace("å", "a").replace("ä", "a").replace("ö", "o").replace(" ", "-")

def get_file_path_from_slug(slug):
    return "storage/" + slug + ".json"

def get_article(slug):
    # letar efter filen som heter <slug>.json
    file_name = get_file_path_from_slug(slug)
    file = codecs.open(file_name, "r", "UTF-8")
    #Konverterar innehållet från JSON till en dictionary
    content = json.loads(file.read())
    file.close()

    return content


#Nedan listas alla rutter som i slutändan returnerar specifika templates.
@route("/")
def index():
    return template("index")

@route("/articles/create", method="GET")
def show_create_form():
    title = request.query.title
    body = request.query.body
    error = request.query.error
    return template("articles/create", title=title, body=body, error=error)

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
        return template("articles/create", title=title, body=body, error=error)

    if not body:
        error = "You must enter the article text"
        return template("articles/create", title=title, body=body, error=error)

    slug = create_slug(title)
    save_article(title, body)
    return (show_article(slug))

@route("/articles")
def archive():
    #Ett arkiv som visar upp alla artiklar
    return template("articles/index", articles=get_articles())

@route("/articles/<slug>")
def show_article(slug):
    '''
    Visar upp en specifik artikel. Försöker man surfa in på en icke-existerande
    artikel returneras en errorsida
    '''
    try:
        article = get_article(slug)
    except:
        return template("error")

    return template("articles/show", article=article)

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
