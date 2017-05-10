#!/usr/bin/env python
# -*- coding: utf-8 -*-


from bottle import route, run, template, static_file, redirect, request, error
import random
import os, sys
import codecs
import json
import psycopg2

# connect to database
try:
    conn = psycopg2.connect(dbname="db_project", host="localhost", port="5432")
    print ("Opened database successfully")

except:
    print("Could not connect to database")

cur = conn.cursor()

@route("/")
def index():
	cur.execute("SELECT rubrik,ingress from artikel")
	rows = cur.fetchall()

	return template("index.html", rows=rows)

@route("/create", method="GET")
def show_create_form():

    return template("create.html")

@route("/show", method="GET")
def visa_hela_artikeln():
	cur.execute("SELECT rubrik,ingress,brödtext from artikel")
	artikel = cur.fetchall()

	return template("show.html", artikel=artikel)

@route("/update", method="POST")
def store_article():
    artikelid = random.randint(1,100)
    rubrik = request.forms.get("rubrik")
    ingress = request.forms.get("ingress")
    text = request.forms.get("text")
    publiceringsdatum = request.forms.get("publiceringsdatum")

    kategoriid = "1"

    print(artikelid, rubrik, ingress, text, publiceringsdatum, kategoriid)

    cur.execute("INSERT INTO artikel(artikelid, rubrik, ingress, brödtext, publiceringsdatum, kategoriid) VALUES(%s,%s,%s,%s,%s,%s)",(artikelid, rubrik, ingress, text, publiceringsdatum, kategoriid))
    conn.commit()

    return template("sparad_artikel.html")


@route("/skribent", method="GET")
def skribent():

    return template("skribent.html")

@route("/lagrad_skribent", method="POST")
def lagrad_skribent():
    skribentid = random.randint(1,100)
    namn = request.forms.get("namn")
    personnummer = request.forms.get("personnummer")

    print(skribentid, namn, personnummer)

    cur.execute("INSERT INTO skribent(skribentid, namn, personnummer) VALUES(%s,%s,%s)",(skribentid, namn, personnummer))
    conn.commit()


    return template("lagrad_skribent.html")


@route("/contact")
def contact():
    return template("contact.html")

@route('/static/<filename>')
def server_static(filename):
    # Returnerar statiska filer, t.ex. JS och CSS
    return static_file(filename, root='static')

@error(404)
def error404(error):
    return template("error.html")


run(host="127.0.0.1", port=8080)
