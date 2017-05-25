\set ON_ERROR_STOP on
\c ag7759
Drop database if exists projekt_mörtfors_emma_matilda;
create database projekt_mörtfors_emma_matilda;
revoke alla privileges on database projekt_mörtfors_emma_matilda from public;
\c projekt_mörtfors_emma_matilda;

CREATE TABLE artikel(artikelid INT NOT NULL PRIMARY KEY, rubrik VARCHAR(40), ingress TEXT, brödtext TEXT, publiceringsdatum DATE, fotoid INT, kategoriid INT);

CREATE TABLE skribent(skribentid INT NOT NULL PRIMARY KEY, namn VARCHAR(40), personnummer INT, anteckning VARCHAR(60));

CREATE TABLE skrivenav(skribentid INT NOT NULL, artikelid INT NOT NULL);

CREATE TABLE bild(fotoid INT NOT NULL PRIMARY KEY, altnamn VARCHAR(40), foto text NOT NULL);

CREATE TABLE bildtext(textid INT NOT NULL PRIMARY KEY, btext text NOT NULL);

CREATE TABLE kommentar(kommentarsid INT NOT NULL PRIMARY KEY, datum DATE NOT NULL, tid TIME, signatur VARCHAR(40), artikelid INT NOT NULL);

CREATE TABLE kategori(kategoriid INT NOT NULL PRIMARY KEY, huvudkategori VARCHAR(20) NOT NULL, underkategori VARCHAR(20), underkategori2 VARCHAR(20));

ALTER TABLE artikel
ADD CONSTRAINT FK_artikel
FOREIGN KEY (kategoriid) REFERENCES kategori(kategoriid);

ALTER TABLE artikel
ADD CONSTRAINT FK_bild
FOREIGN KEY (fotoid) REFERENCES bild(fotoid);

ALTER TABLE bildtext
ADD CONSTRAINT FK_bildtext
FOREIGN KEY (textid) REFERENCES bild(fotoid);

ALTER TABLE kommentar
ADD CONSTRAINT FK_kommentar
FOREIGN KEY (artikelid) REFERENCES artikel(artikelid);

ALTER TABLE skrivenav
ADD CONSTRAINT FK_skrivenav
FOREIGN KEY (artikelid) REFERENCES artikel(artikelid);

ALTER TABLE skrivenav
ADD CONSTRAINT FK_skrivenavtva
FOREIGN KEY (skribentid) REFERENCES skribent(skribentid);
