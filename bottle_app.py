#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import get, route, run, template, static_file, redirect, request, error
import random
import os, sys
import psycopg2
import psycopg2.extras as e
import urllib

# connect to database
try:
    conn = psycopg2.connect(dbname="projekt_mörtfors_emma_matilda", host="localhost", port="5432")
    print ("Opened database successfully")

except:
    print("Could not connect to database")

cur = conn.cursor(cursor_factory=e.DictCursor)

@route("/")
def index():
    cur.execute("SELECT artikelid,rubrik,ingress,publiceringsdatum from artikel ORDER BY publiceringsdatum desc")
    artikel = cur.fetchall()
    for r in artikel:
        rubrik = (r["rubrik"])
        ingress = (r["ingress"])
        publiceringsdatum = (r["publiceringsdatum"])
        artikelidpar = (r["artikelid"])

    return template("index.html", artikel=artikel)

@route("/create", method="GET")
def visa_artikel_form():
    #skriver ut de huvudkategorier som går att välja på.
    cur.execute("SELECT huvudkategori from kategori")
    kategori = cur.fetchall()

    #skriver ut skribenter som lagrats i databasen i en dropdown.
    cur.execute("SELECT skribentid from skribent")
    skribent = cur.fetchall()

    #skriver ut de foton som lagrats i databasen i en dropdown,
    cur.execute("SELECT fotoid from bild")
    bild = cur.fetchall()
    conn.commit()

    return template("create.html", skribent=skribent, bild=bild, kategori=kategori)

@route("/show/<artikelidpar>")
def visa_hela_artikeln(artikelidpar):
    cur.execute("SELECT artikel.artikelid, artikel.rubrik, artikel.ingress, artikel.brödtext, skribent.namn, bild.foto from (artikel JOIN skrivenav ON artikel.artikelid = skrivenav.artikelid join skribent on skribent.skribentid = skrivenav.skribentid JOIN bild ON artikel.fotoid = bild.fotoid) where artikel.artikelid = %s", [artikelidpar])
    artikel = cur.fetchall()
    for r in artikel:
        artikelid = (r["artikelid"])
        rubrik = (r["rubrik"])
        ingress = (r["ingress"])
        brödtext = (r["brödtext"])
        skribent = (r["namn"])
        foto = (r["foto"])

    cur.execute("SELECT kommentartext, datum, tid from kommentar where artikelid = %s", [artikelidpar])
    kommentar = cur.fetchall()
    for r in kommentar:
        kommentartext = (r["kommentartext"])
        datum = (r["datum"])
        tid = (r["tid"])


    return template("show.html", artikel=artikel, artikelid=artikelid, kommentar=kommentar, artikelidpar=artikelidpar)

@route("/lagrad_kommentar", method="POST")
def kommentar_anv():
    kommentarsid = random.randint(1,10000)
    kommentartext = request.forms.get("kommentartext")
    datum = request.forms.get("datum")
    tid = request.forms.get("tid")
    signatur = request.forms.get("signatur")
    artikelidpar = '7872'


    cur.execute("INSERT INTO kommentar(kommentarsid, kommentartext, datum, tid, signatur, artikelid) VALUES(%s,%s,%s,%s,%s,%s)",(kommentarsid, kommentartext, datum, tid, signatur, artikelidpar))
    conn.commit()

    return template("lagrad_kommentar.html", artikelid=artikelidpar)

@route("/update", method="POST")
def lagrad_artikel():
    skribentid = request.forms.get("skribentid")
    artikelid = random.randint(1,10000)
    rubrik = request.forms.get("rubrik")
    ingress = request.forms.get("ingress")
    text = request.forms.get("text")
    publiceringsdatum = request.forms.get("publiceringsdatum")
    bild = request.forms.get("bild")
    textid = random.randint(1,10000)
    bildtext = request.forms.get("bildtext")


    cur.execute("INSERT INTO artikel(artikelid, rubrik, ingress, brödtext, publiceringsdatum, fotoid) VALUES(%s,%s,%s,%s,%s,%s)",(artikelid, rubrik, ingress, text, publiceringsdatum, bild))
    cur.execute("INSERT INTO skrivenav(artikelid, skribentid) VALUES(%s,%s)",(artikelid, skribentid))
    cur.execute("INSERT INTO bildtext(textid, btext) VALUES(%s, %s)", (textid, bildtext))
    conn.commit()

    return template("sparad_artikel.html")

@route("/skribent", method="GET")
def skribent():

    return template("skribent.html")

@route("/lagrad_skribent", method="POST")
def lagrad_skribent():
    skribentid = random.randint(1,10000)
    namn = request.forms.get("namn")
    personnummer = request.forms.get("personnummer")


    cur.execute("INSERT INTO skribent(skribentid, namn, personnummer) VALUES(%s,%s,%s)",(skribentid, namn, personnummer))
    conn.commit()


    return template("lagrad_skribent.html")

@route("/bild")
def contact():

    return template("bild.html")

@route("/lagrad_bild", method="POST")
def lagrad_bild():
    fotoid = random.randint(1,10000)
    altnamn = request.forms.get("altnamn")
    foto = request.forms.get('foto')

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
