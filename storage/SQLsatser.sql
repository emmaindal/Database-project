\set ON_ERROR_STOP on
\c ag7759
Drop database if exists projekt_mörtfors_emma_matilda;
create database projekt_mörtfors_emma_matilda;
revoke alla privileges on database projekt_mörtfors_emma_matilda from public;
\c projekt_mörtfors_emma_matilda;

CREATE TABLE artikel(artikelid SERIAL NOT NULL PRIMARY KEY, rubrik VARCHAR(40), ingress TEXT, brödtext TEXT, publiceringsdatum DATE, kategoriid INT);

CREATE TABLE skribent(skribentid SERIAL NOT NULL PRIMARY KEY, namn VARCHAR(40), personnummer VARCHAR(12), anteckning VARCHAR(60));

CREATE TABLE artikel_skribent(skribentid INT NOT NULL, artikelid INT NOT NULL, PRIMARY KEY(skribentid, artikelid));

CREATE TABLE bild(bildid SERIAL NOT NULL PRIMARY KEY, altnamn VARCHAR(40), foto text NOT NULL);

CREATE TABLE artikel_bild(artikelid INT NOT NULL, bildid INT NOT NULL, bildtext text NOT NULL, PRIMARY KEY(artikelid, bildid));

CREATE TABLE kommentar(kommentarsid SERIAL NOT NULL PRIMARY KEY, kommentartext text, datum DATE NOT NULL, tid TIME, signatur VARCHAR(40), artikelid INT NOT NULL);

CREATE TABLE kategori(kategoriid SERIAL NOT NULL PRIMARY KEY, huvudkategori VARCHAR(20) NOT NULL, underkategori VARCHAR(20), underkategori2 VARCHAR(20));

ALTER TABLE artikel
ADD CONSTRAINT FK_artikel
FOREIGN KEY (kategoriid) REFERENCES kategori(kategoriid);

ALTER TABLE kommentar
ADD CONSTRAINT FK_kommentar
FOREIGN KEY (artikelid) REFERENCES artikel(artikelid);

ALTER TABLE artikel_skribent
ADD CONSTRAINT FK_artikel_skribent_artikel
FOREIGN KEY (artikelid) REFERENCES artikel(artikelid);

ALTER TABLE artikel_skribent
ADD CONSTRAINT FK_artikel_skribent_skribent
FOREIGN KEY (skribentid) REFERENCES skribent(skribentid);

ALTER TABLE bild
ADD CONSTRAINT FK_artikel_bild
FOREIGN KEY (bildid) REFERENCES bild(bildid);
