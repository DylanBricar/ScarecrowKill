# ----------------------------------------------------------------
# -------------- FONCTION DIVERSES
# ----------------------------------------------------------------


class Divers:
    staticSynthese = []  # Permet le transfert des informations d'une class à l'autre

    def pl(nb):
        """ Ajoute un 's' aux mots en fonction du nombre """
        if int(nb) > 1: return 's'
        return ''

    def ratio(kill, dead):
        """ Calcule un ratio """
        if int(dead) == 0:  # Si les morts sont à 0 (on ne peut pas diviser par 0)
            if int(kill) > 0:  # On vérifie le nombre de kill, s'il est supérieur à 0
                # On défini le nombre de kill en étant le ratio
                ratio = round(float(kill), 2)
            else:  # On défini le ratio à 0 étant donné que c'est 0|0
                ratio = 0.0
        else:  # Les morts sont supérieurs à 0
            ratio = round(int(kill) / int(dead), 2)

        return ratio