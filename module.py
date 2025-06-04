# CSV Data Manipulation Module
# -------------------------------------
# This script:
# 1. Modelise in OOP a column of a csv file and an entire csv file
# 2. Cleans and processes the data
# 3. Saves to CSV and JSON file
# 4. Do some stats calculate
# 5. etc.

#import requires
import json
from statistics import mean, median, mode, stdev
import csv
from typing import List



class ColumnData:
    """ 
    This modelise a column of a csv file
    
    """
    def __init__(self, nom : str, data : list):
        
        self.nom = nom
        self.data = data
        self.typ = self.detecter_type()

    def detecter_type(self):

        """Method to dect the type of the elements of a column """
        try:
            [int(v) for v in self.data]
            return int
        except:
            try:
                [float(v) for v in self.data]
                return float
            except:
                return str  
    
    def unique(self) -> list:
        """Method to determine the unique element of a column"""

        list_of_unique = []
        for donnee in self.data:
            if donnee not in list_of_unique:
                list_of_unique.append(donnee)
        return list_of_unique

    def value_counts(self):
        """Method to determine the frequence of each element  of a column"""

        dict_of_value_freq = {}
        for donnee in self.data:
            if donnee not in dict_of_value_freq.keys():
                dict_of_value_freq[donnee] = 1
            else:
                dict_of_value_freq[donnee] += 1
        return dict_of_value_freq

    def stats(self):
        """Method to calculate some stats of a column depending on its type"""

        if self.typ in (int, float):
            moyenne = mean(self.data)
            mediane = median(self.data)
            maximum = max(self.data)
            minimum = min(self.data)
            ecart_type = stdev(self.data)
            return f"Statistique de la colonne \"{self.nom}\"\nMoyenne : {moyenne:.2f}\nMédiane \
                  : {mediane}\nMaximum : {maximum}\nMinimum : {minimum}\nEcart type : {ecart_type:.2f}"
        
        elif self.typ is str:
            mod = mode(self.data)
            nbr_valeur_unique = len(self.unique())
            return f"Mode : {mod}\nNombre de valeurs uniques : {nbr_valeur_unique}"
    
    def __repr__(self):
        return f"Colonne : {self.nom}, {self.data}"


class ClientData:
    """ 
    This modelise a complete csv file
    
    """

    def __init__(self, nom_colonnes: list, dimension: list, lignes : List[list], colonnes : List[ColumnData]):
        self.nom_colonnes = nom_colonnes
        self.dimension = dimension
        self.lignes = lignes
        self.colonnes = colonnes

    def get_colonne(self, nom:str) -> ColumnData | None:
        """Method to get the data of a column using its name"""

        for col in self.colonnes:
            if col.nom == nom:
                return col
        return print(f"aucune colonne associée au nom {nom}")
    
    def get_line(self, index):
        """Method to get the data of a line using its index"""

        if index >= 0 and index <= len(self.lignes)  :
            return self.lignes[index]
        return f"aucune ligne associée à l'index {index}"
    
    def file_over_view(self):
        """Method to see an over view of the file"""

        for nom_colonne in self.nom_colonnes:
            print(f"{nom_colonne:^10}|", end="")
        print()
        print("_"*len(self.nom_colonnes)*11)
        
        for i, ligne in enumerate(self.lignes):
            if i > 5 : 
                break
            for element in ligne :
                print(f"{element:^10}|", end="")
            print()
            print("_"*len(self.nom_colonnes)*11)

    def save_data(self, format) -> None:
        """Method to save the cleaned data in a csv or json file"""
        
        if format == "csv":
            with open("cleaned_client_data.csv", "w", newline='') as f_csv:
                writer = csv.writer(f_csv)
                writer.writerow(self.nom_colonnes)
                writer.writerows(self.lignes)
            print("fihicer nettoyé et sauvegardé en csv")
        elif format == "json":
            list_dict_data = []
            for ligne in self.lignes:
                list_dict_data.append(dict(zip(self.nom_colonnes, ligne)))
            with open("cleaned_client_data.json", "w") as f_json:
                json.dump(list_dict_data, f_json, indent=2)
            print("fihicer nettoyé et sauvegardé en json")
        
    
    def __repr__(self):
        return f"Infos générales du CSV :\nDimension : {self.dimension},\nNom des colonnes : {self.nom_colonnes}"


def convertir(val):
    """Function to convert data in their original type"""
    try:
        if val.isdigit():
            return int(val)
        return float(val)
    except ValueError:
        return val.strip()

def load_csv(file_path) -> ClientData:
    """Function to load csv file"""

    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        lignes = list(reader)
    if lignes :
        nom_colonnes = lignes[0]
        nb_colonnes = len(nom_colonnes)
        nb_lignes = len(lignes) - 1 if len(lignes) > 1 else 0
        dimension = [nb_lignes, nb_colonnes]
        lignes_donnees = lignes[1:]
        donnees_converties = [
            [convertir(val) for val in ligne] for ligne in lignes_donnees
            ]
        lignes_donnees = donnees_converties
        csv_colonnes = list(map(list, zip(*donnees_converties)))
        colonnes_dict = dict(zip(nom_colonnes, csv_colonnes))
        column_data = [ColumnData(key, value) for key, value in colonnes_dict.items()]
    else:
        print("le fichier est vide")

    client_data = ClientData(nom_colonnes, dimension, lignes_donnees, column_data) # type: ignore
    return client_data


def firts_preprocess_data(client_data : ClientData) -> ClientData:
    """
    Function to preprocess data (deleting empty row with >10 null values and 
    replace column null values by the column mean or mode according to the column data type ,..)

    """

    #suppression de ligne avec au moins 10 valeurs manquantes
    for donnees in client_data.lignes:
        missed_value = 0
        for donnee in donnees :
            if not donnee:
                missed_value +=1
        if missed_value >= 10:
            client_data.lignes.remove(donnees)
    client_data.dimension[0] = len(client_data.lignes) #nouvelle valeur du nombre de ligne

    #récupération des nouvelles colonnes après supression des lignes contenant des valeurs manquantes
    liste_colone = list(zip(*client_data.lignes))
    for i, colonne in enumerate(client_data.colonnes):
        colonne.data = liste_colone[i] # type: ignore


    #remplacement des valeurs 999 par -1
    for colonne in client_data.colonnes:
        if colonne.nom == "pdays":
            for i, element in enumerate(colonne.data) :
                if element == 999:
                    colonne.data[i] = -1
    
    #remplacement des valeurs manquantes des colonnes par la moyenne ou le mode selon le type
    for colonne in client_data.colonnes:
        not_none_value = [value for value in colonne.data if value is not None]

        if colonne.typ is int or colonne.typ is float:
            moyenne = mean(not_none_value)
            colonne.data = [moyenne if value is None else value for value in colonne.data]

        elif colonne.typ is str:
            mod = mode(not_none_value)
            colonne.data = [mod if value is None else value for value in colonne.data]
    
    #Nouvelles valeurs lignes après le traitement des colonnes.
    liste_colone = []
    for colonne in client_data.colonnes :
        liste_colone.append(colonne.data)
    client_data.lignes = list(zip(*liste_colone)) # type: ignore
    
    return client_data


def preprocess_data(client_data : ClientData) -> ClientData:
    """Function to preprocess data (cleaning,..)"""

   # Remplacement des mois par des valeurs numériques
    mois_map = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4,
        "may": 5, "jun": 6, "jul": 7, "aug": 8,
        "sep": 9, "oct": 10, "nov": 11, "dec": 12
        }
    
    for colonne in client_data.colonnes:
        #colonne.data = [convertir(v) for v in colonne.data]
        if colonne.nom == "month":
            colonne.data = [mois_map.get(m) for m in colonne.data] # type: ignore

    #Conversion en valeurs numériques des colonnes catégorielles avec nombre de valeur unique d'au plus 12
    for colonne in client_data.colonnes :
        if colonne.nom != "month" and colonne.typ is str and len(colonne.unique()) <= 12 :
            unique_list = colonne.unique()
            map_dict = dict(zip(unique_list, list(range(len(unique_list)))))
            colonne.data = [map_dict.get(cat) for cat in colonne.data]
    
    #Nouvelles valeurs lignes après le traitement des colonnes.
    liste_colone = []
    for colonne in client_data.colonnes :
        liste_colone.append(colonne.data)
    client_data.lignes = list(zip(*liste_colone)) # type: ignore
    
    return client_data


def filter_by_age(age_data : list, min_age : int , max_age : int ) -> None:
    """
    Function to filter the age column
        args :
            age_data : list of age
            min_age : minimu age to filter based on
            max_age : maximum age to filter based on
    """
    age_filtered = []
    for age in age_data:
        if min_age < age < max_age:
            age_filtered.append(age)
    print(f"Nombre d'âges compris entre {min_age} ans et {max_age} ans est {len(age_filtered)}:\n{age_filtered}")


def calculate_subscription_rate(y_data) -> float:
    """
    Function to calculte the client subscription rate
        args :
            y_data : list of client subrsciton
    """
    cpt_y = 0
    for y in y_data :
        if y == "yes":
            cpt_y +=1
    sub_rate = (cpt_y/len(y_data))*100
    return sub_rate


def most_common_job(job_data:dict) -> tuple:
    """
    Function to determine the most frequent job of clients
        args :
            job_data : list of client job
    """

    job_data_ordered =  sorted(job_data.items(), key=lambda  item: item[1], reverse=True)
    most_job = job_data_ordered[0]
    return most_job

