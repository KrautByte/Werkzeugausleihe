import mariadb
from flask import Flask, render_template, request, redirect, url_for

config = {
    'host': 'db.example.com',
    'port': 3306,
    'user': 'ausleihe',
    'password': 'SuperGeheimesKennwort',
    'database': 'WerkzeugAusleihe'
}

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/werkzeuge', methods=['GET', 'POST'])
def werkzeuge():
    if request.method == 'GET':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT * FROM werkzeug')
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(result)
        cur.close()
        conn.close()
        return render_template('werkzeuge.html', tabelle=json_data)
    elif request.method == 'POST':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute('INSERT INTO werkzeug (bezeichnung, beschreibung) VALUES (?,?)',
                    (request.form['Bezeichnung'], request.form['Beschreibung']))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('werkzeuge'))


@app.route('/lieferanten', methods=['GET', 'POST'])
def lieferanten():
    if request.method == 'GET':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT * FROM lieferant')
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(result)
        cur.close()
        conn.close()
        return render_template('lieferanten.html', tabelle=json_data)
    elif request.method == 'POST':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO lieferant (firma, ansprechpartnerName, ansprechpartnerEmail, ansprechpartnerTelefon) VALUES (?,?,?,?)',
            (request.form['Firma'], request.form['Name'], request.form['Email'], request.form['Telefonnummer']))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('lieferanten'))


@app.route('/mitarbeiter', methods=['GET', 'POST'])
def mitarbeiter():
    if request.method == 'GET':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT * FROM mitarbeiter')
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(result)
        cur.close()
        conn.close()
        return render_template('mitarbeiter.html', tabelle=json_data)
    elif request.method == 'POST':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute('INSERT INTO mitarbeiter (nachname, vorname,geburtsdatum) VALUES (?,?,?)',
                    (request.form['Nachname'], request.form['Vorname'], request.form['Geburtstag']))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('mitarbeiter'))


@app.route('/ausleihen', methods=['GET', 'POST'])
def ausleihen():
    if request.method == 'GET':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT * FROM werkzeugausleihe')
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(result)
        cur.close()
        conn.close()
        return render_template('ausleihen.html',
                               tabelle=json_data)
    elif request.method == 'POST':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO werkzeugausleihe (exemplarnr, mitarbeiternr, ausleihdatum, rueckgabedatum, zurueckgegebenam) VALUES (?,?,?,?,?)',
            (request.form['ExemplarNr'], request.form['MitarbeiterNr'], request.form['AusleihDatum'],
             request.form['RueckgabeDatum'], request.form['ZurueckGegebenAm']))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ausleihen'))


@app.route('/combined', methods=['GET', 'POST'])
def combined():
    if request.method == 'GET':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute('SELECT * FROM werkzeuglieferant')
        rv = cur.fetchall()
        json_data = []
        for result in rv:
            json_data.append(result)
        cur.close()
        conn.close()
        return render_template('werkzeuglieferant.html',
                               tabelle=json_data)
    elif request.method == 'POST':
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO werkzeuglieferant (exemplarnr, lieferantennr, anschaffungsdatum, anschaffungspreis , werkzeugnr) VALUES (?,?,?,?,?)',
            (request.form['ExemplarNr'], request.form['LieferantNr'], request.form['AnschaffungsDatum'],
             request.form['AnschaffungsPreis'], request.form['WerkzeugNr']))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('combined'))


if __name__ == '__main__':
    app.run()
