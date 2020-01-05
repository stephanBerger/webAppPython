import mysql.connector
from difflib import SequenceMatcher
from difflib import get_close_matches
import re

con = mysql.connector.connect(
    user="ardit700_student",
    password="ardit700_student",
    host="108.167.140.122",
    database="ardit700_pm1database"
)

def traduction(mot):
    #connexion au serveur de bdd
    cursor = con.cursor()
    #requete pour selectionner tous les mots du dico afin de faire une recherche dessus
    query = cursor.execute("SELECT Expression FROM Dictionary")
    listDeMot = cursor.fetchall();
    tab = [x[0] for x in listDeMot]
    #on cherche le mot le plus ressemblant minimum 0.8 cad 80% de concordance
    motTest = get_close_matches(mot,tab, cutoff=0.8)
    
    if mot in tab:
        return rechercheMot(mot)
    elif mot.lower() in tab:
        return rechercheMot(mot.lower())
    
    elif mot.upper() in tab:
        return rechercheMot(mot.upper())
    
    elif mot.title() in tab:
        return rechercheMot(mot.title())
    
    elif len(motTest)>0:
        #calcul du ration de ressemblance
        s = SequenceMatcher(None,mot,motTest[0])
        taux =round(s.ratio(), 3)
        reponse = input("Ce mot ressemble à {} /100 à {} c'est ce que vous vouliez dire: O pour oui , N pour non ? ".format(taux*100 ,motTest[0]))
    
        if reponse.lower() == 'o':
            return rechercheMot(motTest[0])
        else:
            return "Le mot n'est pas dans la base de donnée !!"
    else:
        return "Le mot n'est pas dans la base de donnée !!"

def rechercheMot(mot):
    cursor = con.cursor()
    query = cursor.execute("SELECT Definition FROM Dictionary WHERE Expression ='%s' " % mot)
    results = cursor.fetchall()
    return results


def miseEnPage(laListe):
    
    if len(laListe) > 0:
        return "\n".join(map(str,(x[0] for x in laListe)))
    else:
        return laListe
    
    
mot = input("Saisissez un mot en anglais: ")

print(miseEnPage(traduction(mot)))