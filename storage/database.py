cursor = connection.cursor()
cursor.execute('''INSERT INTO artikel(artikelid, rubrik, ingress, brödtext, publiceringsdatum, fotoid, kategoriid) VALUES({rubrik}, '{ingress}', '{brödtext}', {})
               '''.format(43, 'hello world'))
connection.commit()

cursor.execute("SELECT * FROM artikel")
print(cursor.fetchall())
connection.close()
