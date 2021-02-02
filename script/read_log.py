#!/usr/bin/env python3

import os
import sys
import pprint
import logging

logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)

# Structures de données
# Tous les résultats sont contenus dans des dictionnaires imbriqués de données

# Main script

logging.debug ("-- Début du script")
logging.debug ("-- Termid %s", os.ctermid())

# L'art du pprint pour afficher les objets Python
pp = pprint.PrettyPrinter(indent=1, width=200, depth=None, stream=None, compact=False, sort_dicts=False)

# Construit la liste des dossiers à parcourir
os.chdir("../data")
logging.debug ("\n")
logging.debug ("1-- Les répertoires suivants seront analysés")

# Tous les résultats seront stockés dans un dictionnaire de dictionnaires
root_rep = {}
for current_file in os.listdir():
    if (os.path.isdir(current_file)):
        root_rep[current_file] = {}
    
logging.debug(str(root_rep))

# Construit la liste des terminaux à analyser
logging.debug("\n")
logging.debug("2-- Analyse de deuxième niveau")

for current_file in root_rep:
    logging.debug("2-- Analyse de", current_file)
    os.chdir(current_file)

    logging.debug(str(root_rep))

    terminal_list={}
    logging.debug (os.listdir())
    for current_terminal in os.listdir():
        if (os.path.isdir(current_terminal)):
            #terminal_list.append(current_terminal)
            terminal_list[current_terminal] = 0

    root_rep[current_file] = terminal_list

    logging.debug(terminal_list)
    logging.debug(len(terminal_list), "terminaux trouvés dans", current_file)

    logging.debug("\n")
    logging.debug("3-- Analyse de troisième niveau")
    for current_terminal in terminal_list:
        logging.debug("\n")
        logging.debug("Analyse du terminal ", current_terminal)
        os.chdir(current_terminal)
        logging.debug("Travail dans le répertoire ", current_terminal)

        print("---")
        print("Terminal", current_terminal)

        # Teste si le terminal a des logs disponibles
        current_file_structure = os.listdir()
        if 'export' in current_file_structure:
            logging.debug("Ce terminal a un répertoire export")

            # Remise à 0 des compteurs pour un terminal donné
            num_paiement_accepte = 0
            num_paiement_refuse = 0
            num_incid_technique = 0
            num_erreur = 0

            # Dictionnaire des patterns
            patterns = {"PAIEMENT ACCEPTE":num_paiement_accepte,"PAIEMENT REFUSE":num_paiement_refuse,"INCID TECHNIQUE":num_incid_technique,"ERREUR":num_erreur, "Fichiers avec incidents":[],"Fichiers avec erreurs":[]}

            # Liste des fichiers sujets à analyse
            fichiers_avec_incidents = []
            fichiers_avec_erreurs = []

            os.chdir("export")
            for current_zip_file in os.listdir():
                file_name, file_extension = os.path.splitext(current_zip_file)
                logging.debug (file_name, ".", file_extension)


                if (file_extension == ".ZIP"):

                    print("  ", current_zip_file)

                    # Décompression du fichier trouvé
                    logging.debug ("Fichier ZIP disponible")
                    logging.debug ("Décompression du fichier", current_zip_file)
                    # Commande linux sioux pour décompresser le maudit fichier zip
                    system_command = "cat \"" + current_zip_file + "\"" + " | gunzip > " + "\"" + file_name + ".TXT\""
                    os.system(system_command)

                    # Analyse du fichier trouvé

                    # Cherche 'PAIEMENT ACCEPTE
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep -n \"'PAIEMENT ACCEPTE\""
                    logging.debug(system_command)
                    result = os.popen(system_command).readlines()
                    logging.debug(result)
                    number_lines=len(result)

                    logging.debug("===> Nombre de lignes du grep ", number_lines)
                    if number_lines > 0:
                        logging.debug("Pattern trouvé")
                        # Ajout du pattern dans le dictionnaire
                        num_paiement_accepte = num_paiement_accepte + number_lines
                        patterns["PAIEMENT ACCEPTE"] = num_paiement_accepte

                    # Cherche 'PAIEMENT REFUSE
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep -n \"'PAIEMENT REFUSE\""
                    logging.debug(system_command)
                    result = os.popen(system_command).readlines()
                    logging.debug(result)
                    number_lines=len(result)

                    if number_lines > 0:
                        logging.debug("Pattern trouvé")
                        # Ajout du pattern dans le dictionnaire
                        num_paiement_refuse = num_paiement_refuse + number_lines
                        patterns["PAIEMENT REFUSE"] = num_paiement_refuse

                    # Cherche INCID TECHNIQUE
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep -n \"'INCID TECHNIQUE\""
                    logging.debug(system_command)
                    result = os.popen(system_command).readlines()
                    logging.debug(result)
                    number_lines=len(result)

                    if number_lines > 0:
                        logging.debug("Pattern trouvé")
                         # Ajout du pattern dans le dictionnaire
                        num_incid_technique = num_incid_technique + number_lines
                        patterns["INCID TECHNIQUE"] = num_incid_technique   

                        # Ajout du fichier incriminé
                        patterns["Fichiers avec incidents"].append(file_name)
                        for i in range(number_lines):
                            patterns["Fichiers avec incidents"].append(str(result[i])[0:20])
                        
                    # Cherche ERREUR
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep -n \"ERREUR\""
                    logging.debug(system_command)
                    result = os.popen(system_command).readlines()
                    logging.debug(result)
                    number_lines=len(result)

                    if number_lines > 0:
                        logging.debug("Pattern trouvé")
                         # Ajout du pattern dans le dictionnaire
                        num_erreur = num_erreur + number_lines
                        patterns["ERREUR"] = num_erreur

                        # Ajout du fichier incriminé
                        patterns["Fichiers avec erreurs"].append(file_name)
                        for i in range(number_lines):
                            patterns["Fichiers avec erreurs"].append(str(result[i])[0:20])

            # Un terminal a été traité
            terminal_list[current_terminal] = patterns
            root_rep[current_file] = terminal_list

            # Remonte au dessus d'export
            os.chdir("..")
            
        else:
            logging.debug("Ce terminal n'a pas de répertoire export")

        # Remonte au dessus du terminal
        os.chdir("..")

    os.chdir("..")

# Résultat final
print("\n**************************************************")
pp.pprint(root_rep)
print("\n**************************************************")