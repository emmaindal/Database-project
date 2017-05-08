CREATE DATABASE projekt_mörtfors_emma_matilda;

CREATE TABLE artikel(artikelid INT NOT NULL PRIMARY KEY, rubrik VARCHAR(40) NOT NULL, ingress TEXT NOT NULL, brödtext TEXT NOT NULL, publiceringsdatum DATE NOT NULL, skribentid INT NOT NULL, fotoid INT, kategoriid INT NOT NULL);

CREATE TABLE skribent(skribentid INT NOT NULL, namn VARCHAR(40) NOT NULL, personnummer INT NOT NULL PRIMARY KEY, anteckning VARCHAR(60));

CREATE TABLE bild(fotoid INT NOT NULL PRIMARY KEY, altnamn VARCHAR(40) NOT NULL, foto bytea NOT NULL);

CREATE TABLE bildtext(textid INT NOT NULL PRIMARY KEY, btext text NOT NULL);

CREATE TABLE kommentar(kommentarsid INT NOT NULL PRIMARY KEY, datum DATE NOT NULL, tid TIME, signatur VARCHAR(40), artikelid INT NOT NULL);

CREATE TABLE kategori(kategoriid INT NOT NULL PRIMARY KEY, huvudkategori VARCHAR(20) NOT NULL, underkategori VARCHAR(20));

ALTER TABLE artikel
ADD CONSTRAINT FK_artikel
FOREIGN KEY (kategoriid) REFERENCES kategori(kategoriid);

ALTER TABLE artikel
ADD CONSTRAINT FK_skribent
FOREIGN KEY (skribentid) REFERENCES skribent(personnummer);

ALTER TABLE artikel
ADD CONSTRAINT FK_bild
FOREIGN KEY (fotoid) REFERENCES bild(fotoid);

ALTER TABLE bildtext
ADD CONSTRAINT FK_bildtext
FOREIGN KEY (textid) REFERENCES bild(fotoid);

ALTER TABLE kommentar
ADD CONSTRAINT FK_kommentar
FOREIGN KEY (artikelid) REFERENCES artikel(artikelid);

CREATE TABLE skrivenav(artikelid INT NOT NULL, skribentid INT NOT NULL);

ALTER TABLE skrivenav
ADD CONSTRAINT FK_skrivenav
FOREIGN KEY (artikelid) REFERENCES artikel(artikelid);

ALTER TABLE skrivenav
ADD CONSTRAINT FK_skrivenavtva
FOREIGN KEY (skribentid) REFERENCES skribent(personnummer);

INSERT INTO skribent
VALUES (2, 'Matilda', 920611)

INSERT INTO artikel VALUES(1, 'Pizza', 'Pizza är gott', 'Pizza är en himla härlig måltid', '2017-05-03', NULL, 1);

INSERT INTO artikel VALUES(2, 'Tacos', 'Tacos är en fredagsrätt', 'Tacos är en himla bra rätt som bara äts på fredagar', '2017-05-05', NULL, 2);
