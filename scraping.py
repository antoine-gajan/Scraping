import requests
import re

def getDataWebsite(url : str):
    """Fonction qui renvoie le code d'un site web"""
    try:
        reponse = requests.get(url)
    except:
        print("Erreur dans la lecture de la page.")
    else:
        return reponse

def getOtherURL(rep):
    """Fonction qui renvoie les liens contenus dans une page"""
    try:
        urls = re.findall(r'href="([^"]+)"', rep.text)
    except:
        print("Erreur dans la récupération des URLs filles.")
    else:
        return list(set(urls))

def getEmailAddress(rep):
    """Fonction qui renvoie l'ensemble des adresses mail uniques d'une page d'un site"""
    try:
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", rep.text)
    except:
        print("Erreur dans la récupération des emails.")
    else:
        return list(set(emails))

def getPhoneNumbers(rep):
    """Fonction qui renvoie l'ensemble des numéros de téléphone"""
    try:
        phone_numbers = re.findall(r"^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$", rep.text)
    except:
        print("Erreur dans la récupération des numéros de téléphone.")
    else:
        return list(set(phone_numbers))

def getInformationDepth(url :str, visited_links : list, email_list : list, phone_list : list, depth = 1):
    "Fonction qui affiche les informations d'une page et des pages associées aux liens contenus avec une certaine profondeur"
    if depth >= 1:
        #Affichage des informations de la page actuelle
        email_list, phone_list = update_information(url, email_list, phone_list)
        visited_links.append(url)
        #Pour chaque lien référencé
        for link in getOtherURL(getDataWebsite(url)):
            #Conversion en adresse absolue
            if not isAbsoluteURL(link) and link != "":
                link = findAbsoluteURL(url, link)
            #Si lien non traité, on affiche ses informations en le traitant
            if link not in visited_links and link != "":
                getInformationDepth(link, visited_links, email_list, phone_list, depth - 1)

def isAbsoluteURL(url : str):
    """Retourne si une URL est absolue"""
    if "://" in url:
        return True
    return False

def findAbsoluteURL(base_url : str, url_relative : str):
    """Retourne l'adresse absolue d'une adresse relative"""
    #Si l'URL est relative
    if not isAbsoluteURL(url_relative):
        #Conversion en absolue
        if url_relative[0] == '/' and base_url[-1] != '/':
            nouv = f"{base_url}{url_relative}"
        if url_relative[0] == '/' and base_url[-1] == '/':
            nouv = f"{base_url}{url_relative[1:]}"
        if url_relative[0] != '/' and base_url[-1] != '/':
            nouv = f"{base_url}/{url_relative}"
        if url_relative[0] != '/' and base_url[-1] == '/':
            nouv = f"{base_url}{url_relative}"
        #Si erreur rencontrée
        if url_relative == "":
            return ""
        #Ajout du slash final
        if nouv[-1] != '/':
            return f"{nouv}/"
        else:
            return f"{nouv}"

def update_information(url : str, email_list : list, phone_list : list):
    """Fonction qui met à jour les informations d'un site web"""
    rep = getDataWebsite(url)
    #Mise à jour des emails de la page
    emails = getEmailAddress(rep)
    email_list = email_list + emails
    #Enlever les doublons
    email_list = list(set(email_list))
    #Mise à jour des numéros de téléphone de la page
    phone_numbers = getPhoneNumbers(rep)
    phone_list = phone_list + phone_numbers
    #Enlever les doublons
    phone_list = list(set(phone_numbers))
    return email_list, phone_list

def print_information(email_list : list, phone_list : list):
    #Affichage des adresses mail
    if email_list != []:
        print("Liste des adresses mail : ")
        for email in email_list:
            print(email)
        print()
    else:
        print("Aucune adresse email trouvée.")
    #Affichage des numéros de téléphone
    if phone_list != []:
        print("Liste des numéros de téléphone : ")
        for phone in phone_list:
            print(phone)
    else:
        print("Aucun numéro de téléphone trouvé.")

def main():
    """Fonction principale"""
    continuer = True
    #Boucle principale
    while continuer:
        #Demande du lien
        url = input("Entrez le lien dont vous souhaitez avec les informations :")
        #Demande de la profondeur
        profondeur = int(input("Profondeur souhaité : "))
        url_visite = []
        email_list = []
        phone_list = []
        #Mise à jour des informations
        getInformationDepth(url, url_visite, email_list, phone_list, profondeur)
        #Affichage des informations
        print_information(email_list, phone_list)
        #Demande pour continuer
        reponse = input("Voulez-vous continuer (O/N) ? ")
        continuer = reponse == 'O'

if __name__ == '__main__':
    main()
