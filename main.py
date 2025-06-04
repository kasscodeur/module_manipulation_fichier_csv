import copy

from module import *




def user_greating() -> None:
    """
        The main function of the programme which allows to test module created 
        to see if it's performed correctly the tasks
    """
    file_path = "bank.csv"
    client_data_csv  = load_csv(file_path)
    client_data =  firts_preprocess_data(client_data_csv)
    client_data_copy = preprocess_data(copy.deepcopy(client_data))
    

    print("Bienvenue dans notre app, quelle opération souhaitiez vous réaliser ? : ")
    while True:
        print("\nQuelle opération souhaitez-vous réaliser ? :")
        print("0 : Infos générales du CVS.")
        print("1 : Obetnir les données d'une colonne.")
        print("2 : Obtenir une ligne à partir de son indexe.")
        print("3 : obtenir les statistiques d'une colonne.")
        print("4 : Aperçu du fichier avec valeurs catégorielles non converties")
        print("5 : Aperçu du fichier avec valeurs catégorielles converties en numériques")
        print("6 : Filtrer les âges.")
        print("7 : Trouver le job le plus courant") #afficher la valeur catégorielle
        print("8 : Obtenir le pourcentage des clients ayant souscrit") #fixer l'erreur
        print("9 : Enregistrer le fihcier traité et nettoyé au format csv ou json")
        print("10 : Quitter")

        while True :
            try :
                user_input = int(input("Votre choix (1-10) : "))
                break
            except ValueError:
                print("Entrée invalide : la valeur saisie doit être un entier")

        if user_input == 0:
            print(client_data)

        elif user_input == 1:
            print(f"liste des colonnes {client_data.nom_colonnes}")
            nom_colonne = input("entrez le nom de la colonne  : ").strip().lower()
            print(client_data.get_colonne(nom_colonne).data) # type: ignore

        elif user_input == 2:
            while True :
                try :
                    index_ligne = int(input("entrez l'indexe de la ligne  : "))
                    break
                except ValueError:
                    print("Entrée invalide : la valeur saisie doit être un entier")
            print(f"Ordre d'affichage des valeurs :\n{client_data.nom_colonnes}")
            print(client_data.get_line(index_ligne))

        elif user_input == 3:
            print(f"liste des colonnes {client_data.nom_colonnes}")
            nom_colonne = input("entrez le nom de la colonne  : ").strip().lower()
            print(client_data.get_colonne(nom_colonne).stats()) # type: ignore

        elif user_input == 4:
            client_data.file_over_view()
        
        elif user_input == 5:
            client_data_copy.file_over_view()

        elif user_input == 6:
            while True :
                try :
                    min_age = int(input("entrez l'age minimal  : "))
                    max_age = int(input("entrez l'age maximal  : "))
                    break
                except ValueError:
                    print("Entrée invalide : la valeur saisie doit être un entier")
            filter_by_age(client_data.get_colonne("age").data, min_age, max_age) # type: ignore

        elif user_input == 7:
            most_job = most_common_job(client_data.get_colonne("job").value_counts())
            print(f"Le job le plus populaire : {most_job}")

        elif user_input == 8:
            sub_rate = calculate_subscription_rate(client_data.get_colonne("y").data)
            print(f"Le pourcenatge des clients ayants soucrit est : {sub_rate:.2f} %")

        elif user_input == 9:
            print("Format de sauvegarde du fichier (csv ou json)")
        
            format = None
            while format not in ["csv", "json"]:
                format = input("Votre choix (csv/json) : ").strip().lower()
                if format not in ["csv", "json"]:
                    print("Format invalide. Veuillez choisir entre 'csv' et 'json'.")

            client_data_copy.save_data(format)

        elif user_input == 10:
            break

        else:
            print("Option invalide. Veuillez choisir un chiffre entre 1 et 5.")
            continue
        while True:
            other_operation = input("Souhaitez vous réaliser une autre opération ? (Oui/Non) : ").title()
            if other_operation == "Oui":
                break
            elif other_operation == "Non":
                return
            else :
                print("Entrée invalide\n")

 

if __name__ == "__main__":
    user_greating()