#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, template, static_file, redirect, request, error
import random
import os, sys
import psycopg2

# connect to database
try:
    conn = psycopg2.connect(dbname="db_project", host="localhost", port="5432")
    print ("Opened database successfully")

except:
    print("Could not connect to database")

cur = conn.cursor()

def skriv_ut_kategorier():
    cur.execute("SELECT huvudkategori, underkategori, underkategori2 from kategori")
    kategori = cur.fetchall()
    print(kategori)

@route("/")
def index():
	cur.execute("SELECT rubrik,ingress,publiceringsdatum from artikel")
	rows = cur.fetchall()

	return template("index.html", rows=rows)

@route("/create", method="GET")
def show_create_form():
    skriv_ut_kategorier()


    #skriver ut skribenter som lagrats i databasen i en dropdown i formuläret.
    cur.execute("SELECT namn from skribent")
    skribent = cur.fetchall()
    print(skribent)

    return template("create.html", skribent=skribent)

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
    namn = request.forms.get("namn")
    personnummer = request.forms.get("personnummer")

    print(namn, personnummer)

    cur.execute("INSERT INTO skribent(namn, personnummer) VALUES(%s,%s)",(namn, personnummer))
    conn.commit()


    return template("lagrad_skribent.html")

@route("/bild")
def contact():

    return template("bild.html")

@route("/lagrad_bild", method="POST")
def lagrad_bild():
    fotoid = random.randint(1,100)
    altnamn = request.forms.get("altnamn")
    url = request.forms.get('url')

    print(fotoid, altnamn, foto)
    cur.execute("INSERT INTO bild(fotoid, altnamn, foto) VALUES(%s,%s,%s)",(fotoid, altnamn, foto))
    conn.commit()

    return template("lagrad_bild.html")

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
