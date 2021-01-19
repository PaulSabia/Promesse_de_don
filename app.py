from flask import Flask, render_template, request, url_for, flash, redirect
from pymongo import MongoClient
import pymongo
import datetime
#from connecteur import Connecteur

class Connecteur:

    @classmethod
    def connection(cls):
        cls.client = MongoClient("mongodb+srv://user:user@promessededon.sw4vx.mongodb.net/database?retryWrites=true&w=majority")
        cls.db = cls.client.PromesseDeDon
        cls.col = cls.db.Dons

    @classmethod
    def deconnection(cls):
        cls.client.close()

    @classmethod
    def insertion(cls, post):
        # Voir pour également insérer la date et l'heure
        cls.connection()
        cls.col.insert_one(post)
        cls.deconnection()

    @classmethod
    def get_db(cls):
        cls.connection()
        result = list(cls.col.find())
        cls.deconnection
        return result

    @classmethod
    def somme_donation(cls):
        cls.connection()
        somme = list(cls.col.aggregate([{'$group': {'_id':'null','montant':{'$sum': '$montant'}}}]))
        somme = somme[0]
        cls.deconnection()
        return somme

    @classmethod
    def get_info(cls, prenom, nom):
        cls.connection()
        info = list(cls.col.find({'prenom': prenom, 'nom': nom}))
        info = info[0]
        cls.deconnection()
        return info

    @classmethod
    def get_donation_user(cls, prenom, nom):
        cls.connection()
        dons = list(cls.col.aggregate([{'$match':{'$and':[{'prenom':prenom},{'nom':nom}]}},{'$group': {'_id':'null','montant':{'$sum': '$montant'}}}]))
        cls.deconnection()
        return dons[0]


# APPLICATION
app = Flask(__name__)
app.config['SECRET_KEY'] = 'madriz'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form', methods=('GET','POST'))
def form():

    if request.method == 'POST':
        prenom = request.form['prenom']
        nom = request.form['nom']
        mail = request.form['mail']
        telephone = request.form['telephone']
        montant = request.form['montant']
        if not prenom or not mail or not telephone or not montant:
            flash('Champs manquant requis !')
        else:
            date = datetime.datetime.now()
            # date = f"{date.day}/{date.month}/{date.year} - {date.hour}:{date.minute}"
            post = {'prenom': prenom, 'nom': nom, 'mail':mail, 'telephone':telephone, 'montant':int(montant), "date": date}
            Connecteur.insertion(post)
            return redirect(url_for('index'))

    return render_template('form.html')

@app.route('/historique')
def historique():
    donnateurs = Connecteur.get_db()
    # donnateurs['date'] = f"{donnateurs['date'].day}/{donnateurs['date'].month}/{donnateurs['date'].year} - {donnateurs['date'].hour}:{donnateurs['date'].minute}"
    somme = Connecteur.somme_donation()
    return render_template('historique.html', donnateurs=donnateurs, somme=somme)

@app.route('/<prenom>/<nom>/admin', methods=('GET','POST'))
def admin(prenom, nom):
    if request.method == 'POST':
        user = request.form['user']
        passwd = request.form['passwd']
        if user=='admin' and passwd=='admin':
            info = Connecteur.get_info(prenom, nom)
            dons = Connecteur.get_donation_user(prenom, nom)
            return render_template('info.html', info=info, dons=dons)
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True)

