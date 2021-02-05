#!/usr/bin/env python3

################################################################################
#
# read_log.py
#
# Script de recherche d'erreurs dans les logs de certaines
# applications bancaires de certains types de terminaux.
#
# https://github.com/franztrierweiler/log_tools
#
# OLAQIN 2021
#
###############################################################################

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
pp = pprint.PrettyPrinter(indent=1, width=150, depth=None, stream=None, compact=False, sort_dicts=False)

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
            num_reboot = 0

            # Dictionnaire des patterns
            patterns = {"PAIEMENT ACCEPTE":num_paiement_accepte, "PAIEMENT REFUSE":num_paiement_refuse,"INCID TECHNIQUE":num_incid_technique,"ERREUR":num_erreur, "REBOOT SUSPECTE":num_reboot, "Fichiers avec incidents":[],"Fichiers avec erreurs":[], "Fichiers avec reboot":[], "Liste jours": {} }

            # Liste des fichiers sujets à analyse
            # A enlever, inutile.
            fichiers_avec_incidents = []
            fichiers_avec_erreurs = []

            liste_jours= {}

            os.chdir("export")
            for current_zip_file in os.listdir():
                file_name, file_extension = os.path.splitext(current_zip_file)
                logging.debug (file_name, ".", file_extension)

                chercher_blocage_terminal = False

                # Fichiers avec stats paiements par jour
                synthese_par_jour = {"Paiements":0,"INCID TECHNIQUE":0,"ERREUR":0}

                # Traitement de chaque fichie ZIP
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
                        synthese_par_jour["Paiements"] = number_lines

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
                        synthese_par_jour["Paiements"] += number_lines

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

                        synthese_par_jour["INCID TECHNIQUE"] = number_lines

                        chercher_blocage_terminal = True
                        
                    # Cherche ERREUR
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep -n \"ERREUR  DE   DIALOGUE\""
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

                        synthese_par_jour["ERREUR"] = number_lines

                        chercher_blocage_terminal = True

                    # S'il y a un incident technique ou une erreur de dialogue, chercher une
                    # trace de reboot dans les traces du fichier en cours.
                    if (chercher_blocage_terminal == True):
                        # Hypothèse #1: un init ADM montre un reboot. 
                        system_command = "cat \"" + file_name + ".TXT\"" + " | grep -n \"Starting C3net server\""

                        logging.debug(system_command)
                        result = os.popen(system_command).readlines()
                        logging.debug(result)
                        number_lines=len(result)

                        if number_lines > 0:
                            logging.debug("Pattern trouvé")
                            # Ajout du pattern dans le dictionnaire
                            num_reboot = num_reboot + number_lines
                            patterns["REBOOT SUSPECTE"] = num_erreur

                            # Ajout du fichier incriminé
                            patterns["Fichiers avec reboot"].append(file_name)
                            for i in range(number_lines):
                                patterns["Fichiers avec reboot"].append(str(result[i])[0:20])

                    liste_jours[file_name[-12:]] = synthese_par_jour

                patterns["Liste jours"] = liste_jours

            # Un terminal a été traité
            # Au moins un fichier ZIP a-t-il été traité ?
            terminal_list[current_terminal] = patterns
            root_rep[current_file] = terminal_list

            # Remonte au dessus d'export
            os.chdir("..")
            
        else:
            logging.debug("Ce terminal n'a pas de répertoire export")
            terminal_list[current_terminal] = ["Aucun log disponible"]
            root_rep[current_file] = terminal_list

        # Remonte au dessus du terminal
        os.chdir("..")

    os.chdir("..")

# Résultat final
print("\n**************************************************")
pp.pprint(root_rep)
print("\n**************************************************")