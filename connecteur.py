from pymongo import MongoClient

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
        result = cls.col.find()
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
    def get_info(cls, _id):
        cls.connection()
        info = cls.col.find()
        return info
