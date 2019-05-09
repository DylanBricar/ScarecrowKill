import sys
sys.path.append("includes\\")

from datetime import datetime
import hashlib
from Divers import Divers


# ----------------------------------------------------------------
# -------------- VERIFICATION DU FICHIER
# ----------------------------------------------------------------

class FileVerificator:
    def __init__(self):
        """ Enregistre le contenu du fichier database.txt dans une variable """
        file = open('database.txt', 'r')
        self.lines = file.readlines()
        file.close()

    def existPseudo(self, value):
        """ Vérifie si dans le fichier ce qui est recherché existe """
        for line in self.lines:
            # Supprime les \n pour éviter les erreurs et découpe la chaine du fichier
            line_file = (line.replace('\n', '')).split('|')

            # Retourne True si le pseudo est trouvé (en minuscule pour éviter les différences maj/min)
            if line_file[0].lower() == value.lower():
                return True
                break

    def addLine(self, pseudo, password):
        """ Ajoute la nouvelle chaine mise à jour dans le fichier """
        # Défini le mot de passe crypté et le style d'écriture utilisé dans le fichier
        password_hash = hashlib.sha1(str.encode(password)).hexdigest()
        pattern = str(pseudo) + '|' + password_hash + '|\n'

        # Ouvre le fichier pour pouvoir récupérer les informations
        file = open('database.txt', 'r')
        old_text = file.read()
        file.close()

        # Ajoute la nouvelle chaine
        new_file = open('database.txt', 'w')
        new_file.write(old_text + pattern)
        new_file.close()

        # Défini le nouveau fichier avec toutes les chaines
        file_back = open('database.txt', 'r')
        self.lines = file_back.readlines()
        file_back.close()

        # Ajoute la date et les points aux informations du fichier
        self.validate(pseudo, password)

    def validate(self, pseudo, password):
        """ Vérifie la validité du pseudo et du mot de passe """
        for line in self.lines:
            # Supprime les \n pour éviter les erreurs et découpe la chaine du fichier
            line_file = (line.replace('\n', '')).split('|')

            # Crée un mot de passe hashé
            password_hash = hashlib.sha1(str.encode(password)).hexdigest()

            # Si le pseudo et le mot de passe sont corrects (on ne fait pas attention aux majuscules dans le pseudo)
            if line_file[0].lower() == pseudo.lower() and line_file[1] == password_hash:
                # Lance la mise à jour, retourne la date de la dernière connexion et stop la boucle
                self.update(line_file)
                return line_file
                break

    def update(self, line_file, point_win=0, point_lost=0):
        """ Mets à jour et ajoute à la variable synthese les informations """
        Divers.staticSynthese = []  # Définie vide pour l'actualisation
        newlines = []  # Liste qui contiendra les nouvelles lignes du fichier
        new_date = datetime.now().strftime('%d/%m/%Y à %Hh%M')  # Format de la date actuelle

        # Boucle qui passe toutes les lignes du fichier database.txt
        for line in self.lines:
            line = (line.replace('\n', ''))  # Supprime les \n pour éviter les erreurs

            # Une connexion a déjÃ  été faite auparavant
            if line_file[2]:
                # Défini la ligne avec laquelle la recherche va se faire
                search = line_file[0] + '|' + line_file[1] + '|' + line_file[2] + '|' + str(line_file[3]) + '|' + str(line_file[4])
                if point_win == 0: point_win = line_file[3]  # Cas où les points sont à 0 alors qu'il a déjÃ  des points
                if point_lost == 0: point_lost = line_file[4]  # Cas où les points sont à 0 alors qu'il a déjÃ  des points
            # C'est la première connexion
            else:
                search = line_file[0] + '|' + line_file[1] + '|'

            # Ligne recherchée trouvée, on l'ajoute au tableau pour le nouveau fichier database.txt
            if line in search:
                newlines.append(line_file[0] + '|' + line_file[1] + '|' + new_date + '|' + str(point_win) + '|' + str(point_lost) + '\n')
            # Ligne recherchée pas trouvée, on recopie tout simplement la ligne dans le tableau
            else:
                newlines.append(line + '\n')

        # Place le tableau newlines dans le fichier database.txt
        with open('database.txt', mode='w') as f:
            f.writelines(newlines)

        # Ajoute à la variable synthese les informations à récupérer dans les autres pages
        Divers.staticSynthese.extend([line_file[0], line_file[1], new_date, point_win, point_lost])

    def classement(self, nb):
        """ Permet de créer le classement en fonction du ratio """
        all_ratio = []  # Les ratio des joueurs
        classement = []  # Les nb meilleurs ratio

        # Enregistre dans une variable le ratio des joueurs
        for line in self.lines:
            line = (line.replace('\n', '')).split('|')
            all_ratio.append(Divers.ratio(int(line[3]), int(line[4])))

        nb_classement_defaut = len(all_ratio)  # Nombre de personne dans le classement

        # Vérifie dans une boucle a qui appartient le plus haut ratio
        for i in range(1, nb+1):

            # S'il y a suffisemment de membre inscrit que demandé dans la fonction
            if nb_classement_defaut >= i:
                maximum_ratio = max(all_ratio)  # Récupère le plus grand ratio

                for line in self.lines:  # Vérifie le fichier
                    line = (line.replace('\n', '')).split('|')  # Coupe la ligne traitée
                    ratio = Divers.ratio(int(line[3]), int(line[4]))  # Récupère le ratio en fonction des réussis/ratés

                    # Vérifie si le plus gros ratio est celui qui est occupé d'être vérifié
                    if ratio == maximum_ratio:
                        classement.append(str(i) + '. ' + str(line[0]) + ' : ' + line[3] + ' - ' + line[4] + ' => ' + str(ratio) + '\n')  # Ajoute dans une variable de classement le résultat
                        all_ratio.remove(ratio)  # Supprime le ratio maximum actuel du tableau avant de le revérifier
            # Il n'y a pas assez de joueur inscrit
            else:
                classement.append(str(i) + '. !!! Place libre !!!\n')  # Ajoute dans une variable de classement le résultat

        return classement