#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bottle import get, route, run, template, static_file, redirect, request, error
import random
import os, sys
import psycopg2
import psycopg2.extras as e

# connect to database
try:
    conn = psycopg2.connect(dbname="projekt_mörtfors_emma_matilda", host="localhost", port="5432")

    print ("Opened database successfully")
    cur = conn.cursor(cursor_factory=e.DictCursor)

except:
    print("Could not connect to database")

@route("/")
def index():
    cur.execute("SELECT artikelid,rubrik,ingress,publiceringsdatum from artikel ORDER BY publiceringsdatum desc")
    artikel = cur.fetchall()

    return template("index.html", artikel=artikel)

@route("/articles/create", method="GET")
def create_article_form():
    #skriver ut de huvudkategorier som går att välja på.
    cur.execute("SELECT huvudkategori from kategori")
    kategori = cur.fetchall()

    #skriver ut skribenter som lagrats i databasen i en dropdown.
    cur.execute("SELECT skribentid,namn from skribent")
    skribent = cur.fetchall()

    #skriver ut de foton som lagrats i databasen i en dropdown,
    cur.execute("SELECT bildid,altnamn from bild")
    bild = cur.fetchall()

    return template("create_article.html", skribent=skribent, bild=bild, kategori=kategori)

@route("/articles", method="POST")
def store_article():
    bild_ids = request.forms.getall("images")
    bild_texter = request.forms.getall("imagetexts")
    bilder = []

    for i in range(0, len(bild_ids)):
        bilder.append({ 'id': bild_ids[i], 'text': bild_texter[i] })

    rubrik = request.forms.get("rubrik")
    ingress = request.forms.get("ingress")
    text = request.forms.get("text")
    publiceringsdatum = request.forms.get("publiceringsdatum")

    cur.execute("INSERT INTO artikel(rubrik, ingress, brödtext, publiceringsdatum) VALUES(%s,%s,%s,%s) RETURNING artikelid",(rubrik, ingress, text, publiceringsdatum))
    artikel_id = cur.fetchone()[0]

    for bild in bilder:
        cur.execute("INSERT INTO artikel_bild (artikelid, bildid, bildtext) VALUES (%s, %s, %s)", (artikel_id, bild["id"], bild["text"]))

    skribentiddata = request.forms.getall("skribentid")
    for skribentid in skribentiddata:
        cur.execute("INSERT INTO artikel_skribent(artikelid, skribentid) VALUES(%s,%s)",(artikel_id, skribentid))

    conn.commit()

    return template("stored_article.html")

@route("/articles/<artikel_id>")
def show_article(artikel_id):
    cur.execute("""
    SELECT artikel.artikelid, artikel.rubrik, artikel.ingress, artikel.brödtext
    FROM artikel
    WHERE artikel.artikelid = %s""", [artikel_id])
    artikel = cur.fetchone()

    cur.execute("SELECT namn FROM skribent JOIN artikel_skribent ON artikel_skribent.skribentid = skribent.skribentid WHERE artikel_skribent.artikelid = %s", [artikel_id])
    authors = ", ".join(map(lambda x: x[0], cur.fetchall()))

    cur.execute("SELECT kommentarsid, signatur, kommentartext, datum, tid from kommentar where artikelid = %s", [artikel_id])
    kommentar = cur.fetchall()

    cur.execute("SELECT foto, altnamn, bildtext FROM artikel_bild JOIN bild ON bild.bildid = artikel_bild.bildid WHERE artikel_bild.artikelid = %s", [artikel_id])
    bilder = cur.fetchall()

    return template("show_article.html", artikel=artikel, authors=authors, kommentar=kommentar, bilder=bilder)

@route("/articles/<artikel_id>/comments", method="POST")
def store_comment(artikel_id):
    kommentartext = request.forms.get("kommentartext")
    datum = request.forms.get("datum")
    tid = request.forms.get("tid")
    signatur = request.forms.get("signatur")
    artikelid = artikel_id

    cur.execute("INSERT INTO kommentar(kommentartext, datum, tid, signatur, artikelid) VALUES (%s,%s,%s,%s,%s)",(kommentartext, datum, tid, signatur, artikelid))
    conn.commit()

    return template("stored_comment.html")

@route("/comments/<kommentar_id>/delete")
def delete_comment(kommentar_id):

    cur.execute("DELETE FROM kommentar WHERE kommentarsid = %s", [kommentar_id])
    conn.commit()

    return template("delete_comment.html")

@route("/authors/create", method="GET")
def create_author_form():
    return template("create_author.html")

@route("/authors", method="POST")
def store_author():
    namn = request.forms.get("namn")
    personnummer = request.forms.get("personnummer")

    cur.execute("INSERT INTO skribent(namn, personnummer) VALUES(%s,%s)",(namn, personnummer))
    conn.commit()

    return template("stored_author.html")

@route("/images/create")
def create_image_form():
    return template("upload_images.html")

@route("/images", method="POST")
def store_image():
    altnamn = request.forms.get("altnamn")
    foto = request.forms.get('foto')

    cur.execute("INSERT INTO bild(altnamn, foto) VALUES(%s,%s)",(altnamn, foto))
    conn.commit()

    return template("stored_images.html")

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
