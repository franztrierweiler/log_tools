#!/usr/bin/env python3

import os
import zipfile

print ("-- Début du script")
print ("-- Termid", os.ctermid())

# Construit la liste des dossiers à parcourir
os.chdir("../data")
print("\n")
print("1-- Les répertoires suivants seront analysés")

root_rep = []
for current_file in os.listdir():
    if (os.path.isdir(current_file)):
        root_rep.append(current_file)
print(root_rep)

# Construit la liste des terminaux à analyser
print("\n")
print("2-- Analyse de deuxième niveau")

for current_file in root_rep:
    print("2-- Analyse de", current_file)
    os.chdir(current_file)

    terminal_list=[]
    for current_terminal in os.listdir():
        if (os.path.isdir(current_terminal)):
            terminal_list.append(current_terminal)
    
    print(len(terminal_list), "terminaux trouvés !")
    print("Terminaux trouvés ", terminal_list)

    print("\n")
    print("3-- Analyse de troisième niveau")
    for current_terminal in terminal_list:
        print("\n")
        print("Analyse du terminal ", current_terminal)
        os.chdir(current_terminal)

        #Teste si le terminal a des logs disponibles
        current_file_structure = os.listdir()
        if 'export' in current_file_structure:
            print("Ce terminal a des logs")
            
            os.chdir("export")
            for current_zip_file in os.listdir():
                file_name, file_extension = os.path.splitext(current_zip_file)
                print (file_name, ".", file_extension)

                if (file_extension == ".ZIP"):
                    print ("Décompression du fichier", file_name)

            os.chdir("..")

        else:
            print("Ce terminal n'a pas de répertoire export")
        
        os.chdir("..")


    os.chdir("..")
        