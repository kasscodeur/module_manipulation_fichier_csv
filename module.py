# CSV Data Manipulation Module
# -------------------------------------
# This script:
# 1. Modelise in OOP a column of a csv file and an entire csv file
# 2. Cleans and processes the data
# 3. Saves to CSV and JSON file
# 4. Do some stats calculate
# 5. etc.

# import requires
import json
from statistics import mean, median, mode, stdev
import csv
from typing import List, Union

from src.utils import convertir


class ColumnData:
    """This class modelise a column of a csv file"""

    def __init__(self, nom: str, data: list):
        self.nom = nom
        self.data = data
        self.typ = self.detecter_type()

    def detecter_type(self):
        """Method to dect the type of the elements of a column"""

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
        """Method to determine the unique element of a column

        Returns:
            list: list of the unique element of the column

        """

        list_of_unique = []
        for donnee in self.data:
            if donnee not in list_of_unique:
                list_of_unique.append(donnee)
        return list_of_unique

    def value_counts(self) -> dict:
        """Method to determine the frequence of each element  of a column

        Returns:
            dict: dict of key value of the element and it frequence
        """

        dict_of_value_freq = {}
        for donnee in self.data:
            if donnee not in dict_of_value_freq.keys():
                dict_of_value_freq[donnee] = 1
            else:
                dict_of_value_freq[donnee] += 1
        return dict_of_value_freq

    def stats(self) -> None:
        """Method to calculate some stats of a column depending on its type

        Returns:
            str: a string of the summary of the column stat
        """

        if self.typ in (int, float):
            moyenne = mean(self.data)
            mediane = median(self.data)
            maximum = max(self.data)
            minimum = min(self.data)
            ecart_type = stdev(self.data)
            print(
                f'\nStatistique de la colonne "{self.nom}"\nMoyenne : {moyenne:.2f}'
                f"\nMédiane : {mediane}\nMaximum : {maximum}\nMinimum : {minimum}"
                f'\nEcart type : {ecart_type:.2f}"\n'
            )

        elif self.typ is str:
            mod = mode(self.data)
            nbr_valeur_unique = len(self.unique())
            print(f"Mode : {mod}\nNombre de valeurs uniques : {nbr_valeur_unique}")

    def __repr__(self):
        return f"Colonne : {self.nom}, {self.data}"


class ClientData:
    """A class to modelise a complete csv file"""

    def __init__(
        self,
        nom_colonnes: list,
        dimension: list,
        lignes: List[list],
        colonnes: List[ColumnData],
    ):
        self.nom_colonnes = nom_colonnes
        self.dimension = dimension
        self.lignes = lignes
        self.colonnes = colonnes

    def get_colonne(self, nom: str) -> ColumnData | str:
        """Method to get the data of a column using its name

        Args:
            nom (str): a column name
        """

        for col in self.colonnes:
            if col.nom == nom:
                return col
        return f"aucune colonne associée au nom {nom}"

    def get_line(self, index: int) -> List[Union[str, int]] | str:
        """Method to get the data of a line using its index

        Args:
            index (int): the index of line to retrive

        Returns:
            list(srt, int) | str: list of a row value
            or a string when index out of range
        """

        if index >= 0 and index <= len(self.lignes):
            return self.lignes[index]
        return f"aucune ligne associée à l'index {index}"

    def file_over_view(self) -> None:
        """Method to see an over view of the file(only the first 5 rows)"""

        for nom_colonne in self.nom_colonnes:
            print(f"{nom_colonne:^10}|", end="")
        print()
        print("_" * len(self.nom_colonnes) * 11)

        for i, ligne in enumerate(self.lignes):
            if i > 5:
                break
            for element in ligne:
                print(f"{element:^10}|", end="")
            print()
            print("_" * len(self.nom_colonnes) * 11)

    def save_data(self, format: str) -> None:
        """Method to save the cleaned data in a csv or json file

        Args:
            format(str): the file format wanted to save (csv or json)
        """

        if format == "csv":
            with open("cleaned_client_data.csv", "w", newline="") as f_csv:
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
        return (
            f"Infos générales du CSV :\nDimension : {self.dimension},"
            f"\nNom des colonnes : {self.nom_colonnes}"
        )


def load_csv(file_path) -> ClientData:
    """Function to load csv file

    Args:
        file_path : the path of the file to load

    Returns:
        object: An instance of ClientData class
    """

    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        lignes = list(reader)
    if lignes:
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

    client_data = ClientData(nom_colonnes, dimension, lignes_donnees, column_data)  # type: ignore
    return client_data


def delete_row_with_nan_values(client_data: ClientData) -> ClientData:
    """Function to remove raws with at leat 10 nan values

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """

    for donnees in client_data.lignes:
        missed_value = 0
        for donnee in donnees:
            if not donnee:
                missed_value += 1
        if missed_value >= 10:
            client_data.lignes.remove(donnees)
    client_data.dimension[0] = len(
        client_data.lignes
    )  # nouvelle valeur du nombre de ligne

    return client_data


def replace_pdays_column_values(client_data: ClientData) -> ClientData:
    """Function to replace 'pdays' column 999 value by -1

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """

    for colonne in client_data.colonnes:
        if colonne.nom == "pdays":
            for i, element in enumerate(colonne.data):
                if element == 999:
                    colonne.data[i] = -1
    return client_data


def replace_nan_values_by_mean_or_mode(client_data: ClientData) -> ClientData:
    """Function to replace nan values by thier mean or mode according to their typ

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """

    for colonne in client_data.colonnes:
        not_none_value = [value for value in colonne.data if value is not None]

        if colonne.typ is int or colonne.typ is float:
            moyenne = mean(not_none_value)
            colonne.data = [
                moyenne if value is None else value for value in colonne.data
            ]

        elif colonne.typ is str:
            mod = mode(not_none_value)
            colonne.data = [mod if value is None else value for value in colonne.data]
    return client_data


def new_col_values_after_preprocess(client_data: ClientData) -> ClientData:
    """Function to update the new values of columns

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """

    liste_colone = []
    for colonne in client_data.colonnes:
        liste_colone.append(colonne.data)
    client_data.lignes = list(zip(*liste_colone))  # type: ignore
    return client_data


def first_preprocess_data(client_data: ClientData) -> ClientData:
    """Function to preprocess data (cleaning,..)

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """

    # suppression de ligne avec au moins 10 valeurs manquantes
    client_data = delete_row_with_nan_values(client_data)

    # récupération des nouvelles colonnes après supression
    # des lignes contenant des valeurs manquantes
    liste_colone = list(zip(*client_data.lignes))
    for i, colonne in enumerate(client_data.colonnes):
        colonne.data = liste_colone[i]  # type: ignore

    # remplacement des valeurs 999 par -1
    client_data = replace_pdays_column_values(client_data)

    # remplacement des valeurs manquantes des colonnes
    # par la moyenne ou le mode selon le type
    client_data = replace_nan_values_by_mean_or_mode(client_data)

    # Nouvelles valeurs lignes après le traitement des colonnes.
    client_data = new_col_values_after_preprocess(client_data)

    return client_data


def replace_monthname_by_value(client_data: ClientData) -> ClientData:
    """Function to mapp each month name with it vlue

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """
    # Remplacement des mois par des valeurs numériques
    mois_map = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }

    for colonne in client_data.colonnes:
        if colonne.nom == "month":
            colonne.data = [mois_map.get(m) for m in colonne.data]  # type: ignore
    return client_data


def transform_num_values_in_cat(client_data: ClientData) -> ClientData:
    """Function to convert into numerical categorical columns value
    if unique values count >12

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """

    for colonne in client_data.colonnes:
        if (
            colonne.nom != "month"
            and colonne.typ is str
            and len(colonne.unique()) <= 12
        ):
            unique_list = colonne.unique()
            map_dict = dict(zip(unique_list, list(range(len(unique_list)))))
            colonne.data = [map_dict.get(cat) for cat in colonne.data]
    return client_data


def preprocess_data(client_data: ClientData) -> ClientData:
    """Function to preprocess data (cleaning,..)

    Args:
        client_data (ClientData): the instance of ClientData to preprocess

    Returns:
        object: An instance of ClientData class
    """

    # Remplacement des mois par des valeurs numériques
    client_data = replace_monthname_by_value(client_data)

    # Conversion en valeurs numériques des colonnes catégorielles
    # avec nombre de valeur unique d'au plus 12
    client_data = transform_num_values_in_cat(client_data)

    # Nouvelles valeurs lignes après le traitement des colonnes.
    client_data = new_col_values_after_preprocess(client_data)
    return client_data


def filter_by_age(age_data: list, min_age: int, max_age: int) -> None:
    """Function to filter the age column

    Args :
        age_data : list of age
        min_age : minimum age to filter based on
        max_age : maximum age to filter based on
    """
    age_filtered = []
    for age in age_data:
        if min_age < age < max_age:
            age_filtered.append(age)
    print(
        f"Nombre d'âges compris entre {min_age} ans"
        f"et {max_age} ans est {len(age_filtered)}:\n{age_filtered}\n"
    )


def calculate_subscription_rate(y_data) -> float:
    """Function to calculte the client subscription rate

    Args :
        y_data : list of client subrsciton

    Returns:
        float: the subscrption rate
    """

    cpt_y = 0
    for y in y_data:
        if y == "yes":
            cpt_y += 1
    sub_rate = (cpt_y / len(y_data)) * 100
    return sub_rate


def most_common_job(job_data: dict) -> tuple:
    """Function to determine the most frequent job of clients

    Args :
        job_data : list of client job

    Returns :
        tuple: tuple of the common job and it count
    """

    job_data_ordered = sorted(job_data.items(), key=lambda item: item[1], reverse=True)
    most_job = job_data_ordered[0]
    return most_job
