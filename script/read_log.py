#!/usr/bin/env python3

import os
import sys

# Structures de données
# Tous les résultats sont contenus dans des dictionnaires imbriqués de données

# Main script

print ("-- Début du script")
print ("-- Termid", os.ctermid())

# Construit la liste des dossiers à parcourir
os.chdir("../data")
print("\n")
print("1-- Les répertoires suivants seront analysés")

# Tous les résultats seront stockés dans un dictionnaire de dictionnaires
root_rep = {}
for current_file in os.listdir():
    if (os.path.isdir(current_file)):
        #root_rep.append(current_file)
        root_rep[current_file] = 0
    
print(str(root_rep))

# Construit la liste des terminaux à analyser
print("\n")
print("2-- Analyse de deuxième niveau")

for current_file in root_rep:
    print("2-- Analyse de", current_file)
    os.chdir(current_file)

    print(str(root_rep))

    terminal_list={}
    print (os.listdir())
    for current_terminal in os.listdir():
        if (os.path.isdir(current_terminal)):
            #terminal_list.append(current_terminal)
            terminal_list[current_terminal] = 0

    root_rep[current_file] = terminal_list

    print(terminal_list)
    print(len(terminal_list), "terminaux trouvés dans", current_file)

    print("\n")
    print("3-- Analyse de troisième niveau")
    for current_terminal in terminal_list:
        print("\n")
        print("Analyse du terminal ", current_terminal)
        os.chdir(current_terminal)
        print("Travail dans le répertoire ", current_terminal)

        # Teste si le terminal a des logs disponibles
        current_file_structure = os.listdir()
        if 'export' in current_file_structure:
            print("Ce terminal a un répertoire export")

            # Remise à 0 des compteurs pour un terminal donné
            num_paiement_accepte = 0
            num_paiement_refuse = 0
            num_incid_technique = 0

            # Dictionnaire des patterns
            patterns = {"PAIEMENT ACCEPTE":num_paiement_accepte,"PAIEMENT REFUSE":num_paiement_refuse,"INCID TECHNIQUE":num_incid_technique}

            os.chdir("export")
            for current_zip_file in os.listdir():
                file_name, file_extension = os.path.splitext(current_zip_file)
                print (file_name, ".", file_extension)

                if (file_extension == ".ZIP"):
                    # Décompression du fichier trouvé
                    print ("Fichier ZIP disponible")
                    print ("Décompression du fichier", current_zip_file)
                    # Commande linux sioux pour décompresser le maudit fichier zip
                    system_command = "cat \"" + current_zip_file + "\"" + " | gunzip > " + "\"" + file_name + ".TXT\""
                    os.system(system_command)

                    # Analyse du fichier trouvé

                    # Cherche 'PAIEMENT ACCEPTE
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep \"'PAIEMENT ACCEPTE\""
                    print(system_command)
                    result = os.system(system_command)
                    print(result)
                    if result == 0:
                        print("Pattern trouvé")
                        # Ajout du pattern dans le dictionnaire
                        num_paiement_accepte = num_paiement_accepte + 1
                        patterns["PAIEMENT ACCEPTE"] = num_paiement_accepte

                     # Cherche 'PAIEMENT REFUSE
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep \"'PAIEMENT REFUSE\""
                    print(system_command)
                    result = os.system(system_command)
                    print(result)
                    if result == 0:
                        print("Pattern trouvé")
                        # Ajout du pattern dans le dictionnaire
                        num_paiement_refuse = num_paiement_refuse + 1
                        patterns["PAIEMENT REFUSE"] = num_paiement_refuse

                    # Cherche INCID TECHNIQUE
                    system_command = "cat \"" + file_name + ".TXT\"" + " | grep \"'INCID TECHNIQUE\""
                    print(system_command)
                    result = os.system(system_command)
                    print(result)
                    if result == 0:
                        print("Pattern trouvé")
                         # Ajout du pattern dans le dictionnaire
                        num_incid_technique = num_incid_technique + 1
                        patterns["INCID TECHNIQUE"] = num_incid_technique

            print("++++++++++++++++++++++++++++++++++++++")
            print(str(patterns))
            print("++++++++++++++++++++++++++++++++++++++")
            terminal_list[current_terminal] = patterns
            root_rep[current_file] = terminal_list

            # Remonte au dessus d'export
            os.chdir("..")
            
        else:
            print("Ce terminal n'a pas de répertoire export")
        
        # Remonte au dessus du terminal
        os.chdir("..")

    os.chdir("..")

# Résultat final
print(str(root_rep))
