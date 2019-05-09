import sys
sys.path.append("includes\\")

from tkinter import Canvas, Frame, Button, PhotoImage, NW
from PIL import Image, ImageTk
from random import randrange
from math import pi, sin, cos
from FileVerificator import FileVerificator
from Divers import Divers


# ----------------------------------------------------------------
# -------------- COMPORTEMENT DU JEU
# ----------------------------------------------------------------

class GameCanon(Frame):
    __angle = 0              # Angle par défaut
    __x_deplace = 15         # Echelle de déplacement du canon
    __dt = 20                # Delta T
    __g = 50                 # Gravité
    __tir = False            # Tir en cours
    __nb_tir = [0, 0]        # Tir [réussi, raté]
    __list_speed = [30, -20]  # Vitesse en X et Y dans une liste pour modifier toutes les valeurs du code d'un coup
    __speed = [__list_speed[0], __list_speed[1] * 0]  # Vitesse X et Y qui sera modifié avec l'angle par la suite
    __reset_speed = [__list_speed[0], __list_speed[1] * 0]  # Vitesse en X et Y à ne pas modifier pour le reset du jeu

    def __init__(self, windows, **kwargs):
        """ Lancement de l'application """
        super().__init__(windows, **kwargs)  # Permet de récupérer les précédents arguments appelés
        self.windows = windows  # Rend la fenêtre importée globale à toute la class
        self.verif = FileVerificator()  # Instancie la includes de vérification des fichiers
        self._create_interface()  # Crée l'interface pour s'inscrire à l'application

    def _create_interface(self):
        """ Création de l'interface graphique """
        # Configuration du Canvas de base (fond, alignement, taille, ...)
        self.game = Canvas(self.windows, width=1200, height=500, highlightthickness=0)
        self.bg_game = ImageTk.PhotoImage(Image.open('ressources/bg_game.png'))
        self.game.create_image(0, 0, image=self.bg_game, anchor='nw')
        self.game.place(x=0, y=0)

        # Place les roues
        self.roues_img = PhotoImage(file='ressources/roues.gif')
        self.roues = self.game.create_image(90, 467, image=self.roues_img)

        # Place le canon
        self.canon_img = PhotoImage(file='ressources/canon.gif')
        self.canon = self.game.create_image(100, 440, image=self.canon_img)

        # Place la cible
        self.cible_img = PhotoImage(file='ressources/cible.gif')
        self.cible = self.game.create_image(randrange(700, 1100), randrange(390, 420), image=self.cible_img)

        # Place l'obus
        self.obus_img = PhotoImage(file='ressources/obus.gif')
        self.obus = self.game.create_image(176, 400, image=self.obus_img)

        # Affiche les tirs et l'angle en haut à gauche
        result_rect = self.game.create_rectangle(10, 10, 250, 120, fill='white')
        info = self.game.create_text(130, 28, fill='darkred', font=('Helvetica', 20, 'bold'), text='Informations', )
        self.result = self.game.create_text(75, 79, font=('Helvetica', 14), text='Tir réussi : {0}\nTir raté : {1}\nAngle : {2}'.format(str(self.__nb_tir[0]), str(self.__nb_tir[1]), str(abs(self.__angle))))

        # Affiche l'angle dans la barre vertical de fond
        fond_anglebar = self.game.create_rectangle(1170, 89, 1190, 400, fill='white')
        self.contenu_anglebar = self.game.create_rectangle(1175, 380, 1185, 390, fill='darkgreen')

        # Superpose les textes sur le rectangle
        self.game.tag_raise(info, result_rect)
        self.game.tag_raise(self.result, result_rect)
        self.game.tag_raise(self.contenu_anglebar, fond_anglebar)

        # Affiche le bouton pour quitter le jeu
        btn_quitter = Button(self.windows, fg='white', bg='#CA994F', text='Revenir à l\'espace membre', command=self.back_member)
        btn_quitter.grid(ipadx=10, ipady=2)
        self.game.create_window(998, 10, anchor=NW, window=btn_quitter)

        # Récupère la touche pressée et l'envoie au routeur
        for i in ['<space>', '<Up>', '<Down>', '<Left>', '<Right>']:
            self.windows.bind(i, self.router)

    def router(self, event):
        """ Réagi en fonction de l'évenement reÃ§u """
        # Tire l'obus en faisant appel à la fonction + vérifie qu'un obus n'est pas déjà lancé
        if event.keysym == 'space' and not self.__tir: self.shoot()

        # Déplace l'angle de tir en fonction des touches pressées (haut ou bas) + vérifie qu'un obus n'est pas déjà lancé
        elif (event.keysym == 'Up' or event.keysym == 'Down') and not self.__tir: self.set_angle(event.keysym)

        # Déplace le canon en fonction des touches pressées (gauche ou droite) + vérifie qu'un obus n'est pas déjà lancé
        elif (event.keysym == 'Left' or event.keysym == 'Right') and not self.__tir: self.deplace(event.keysym)

    def set_angle(self, touche):
        """ Défini l'angle de tir du canon et modifie la barre de l'angle """
        # Recupère les coordonnées de base de la barre de l'angle
        coords = self.game.coords(self.contenu_anglebar)
        new_y_anglebar = coords[1]

        if self.__angle >= 80:  # Si l'angle est supérieur ou égal à 80°, on le réduit
            if touche == 'Down':
                self.__angle -= 2
                new_y_anglebar = coords[1] + 7  # 7 ajouté aux coordonnées du rectangle car 7 est une bonne echelle
        elif self.__angle <= 0:  # Si l'angle est inférieur ou égal à 0*, on l'augmente
            if touche == 'Up':
                self.__angle += 2
                new_y_anglebar = coords[1] - 7
        else:  # Dans le cas oÃ¹ on n'est dans aucune limite, les deux touches fonctionnent
            if touche == 'Up':
                self.__angle += 2
                new_y_anglebar = coords[1] - 7
            if touche == 'Down':
                self.__angle -= 2
                new_y_anglebar = coords[1] + 7

        # Modification des informations pour y ajouter l'angle
        succes = self.__nb_tir[0]  # Tirs réussis
        failed = self.__nb_tir[1]  # Tirs ratés
        self.game.itemconfig(self.result, text='Tir{0} réussi{1} : {2}\nTir{3} raté{4} : {5}\nAngle : {6}'.format(Divers.pl(succes), Divers.pl(succes), str(succes), Divers.pl(failed), Divers.pl(failed), str(failed), str(abs(self.__angle))))

        # Modifie le X et Y avec le nouvel angle
        self.__speed = [self.__list_speed[0] * cos(float(self.__angle) * 2 * pi / 360),
                        self.__list_speed[1] * sin(float(self.__angle) * 2 * pi / 360)]


        # Modifie la barre en éditant la couleur et la nouvelle position
        self.game.coords(self.contenu_anglebar, coords[0], new_y_anglebar, coords[2], coords[3])

        if (self.__angle >= 0) and (self.__angle <= 30):
            self.game.itemconfig(self.contenu_anglebar, fill='darkgreen')
        elif (self.__angle > 30) and (self.__angle <= 50):
            self.game.itemconfig(self.contenu_anglebar, fill='orange')
        elif (self.__angle > 50) and (self.__angle <= 65):
            self.game.itemconfig(self.contenu_anglebar, fill='red')
        elif self.__angle > 70:
            self.game.itemconfig(self.contenu_anglebar, fill='darkred')

    def deplace(self, touche):
        """ Déplace horizontalement le canon, les roues et l'obus collé """
        coords_obus = self.get_coords(self.obus_img, self.obus)  # Coordonnées de l'obus

        # Déplacement vers la droite
        if touche == 'Right':
            # Limite de déplacement imposé à maximum 400px
            if coords_obus[0] < 400:
                # Déplace les objets du nombre de X défini sans toucher au Y
                self.game.move(self.obus, self.__x_deplace, 0)
                self.game.move(self.roues, self.__x_deplace, 0)
                self.game.move(self.canon, self.__x_deplace, 0)
        # Déplacement vers la gauche
        else:
            # Limite de déplacement imposé à minimum 170px
            if coords_obus[0] > 170:
                self.game.move(self.obus, -self.__x_deplace, 0)
                self.game.move(self.roues, -self.__x_deplace, 0)
                self.game.move(self.canon, -self.__x_deplace, 0)

    def shoot(self):
        """ Appelé lors du tir et s'occupe d'actualiser la nouvelle position """
        # Si l'obus touche la cible
        if self.is_impacted():
            # L'obus n'est pas sorti du jeu ou n'a pas touché le sol
            if self.__speed != [0, 0]:
                # Déplace l'obus en bougeant l'image toutes les __dt ms
                self.__speed = self.move_img(self.obus_img, self.obus, self.__speed)
                self.game.move(self.obus, self.__speed[0], self.__speed[1])
                self.game.after(self.__dt, self.shoot)
                self.__tir = True  # Permet de ne pas tirer 2 obus à la fois
            else:
                self.reset(True)  # L'obus a touché sa cible
        else:
            self.reset(False)  # L'obus n'a pas touché sa cible

    def get_coords(self, img, obj):
        """ Récupère les coordonnées des 4 points d'une image """
        # Divise l'image en deux pour y trouver le centre
        halfwidth = img.width() / 2
        halfheight = img.height() / 2
        centre = self.game.coords(obj)

        # Défini les coordonnées des 4 points de l'image et les retourne
        coords = [centre[0] - halfwidth, centre[1] - halfheight, centre[0] + halfwidth, centre[1] + halfheight]
        return coords

    def move_img(self, image, obj, speed):
        """ Gestion de la nouvelle position de l'obus """
        coordonnees = self.get_coords(image, obj)  # Défini les bords de l'image

        # L'obus est sorti de l'espace de jeu
        if (0 >= coordonnees[0]) or (1200 - self.__speed[0] <= coordonnees[2]): newspeed = [0, 0]
        # L'obus est tomné au sol
        elif 0 >= coordonnees[1] or (500 - self.__speed[1] <= coordonnees[3]): newspeed = [0, 0]
        # L'obus est en mouvement
        else: newspeed = [self.__speed[0], self.__speed[1]+int(self.__g*self.__dt/1000)]

        return newspeed  # Nouvelle position

    def is_impacted(self):
        """ Si une collision est repérée """
        # Défini les bords des deux images
        coords_obus = self.get_coords(self.obus_img, self.obus)
        coords_cible = self.get_coords(self.cible_img, self.cible)

        # Action si les bords de l'obus et de la cible se touchent
        if (coords_cible[0] <= coords_obus[0] <= coords_cible[2]) and (coords_cible[1] <= coords_obus[1] <= coords_cible[3]):
            return False  # Touché
        return True  # Pas touché

    def reset(self, resultat):
        """ Remet à zéro le jeu après un tir """
        self.__angle = 0  # Remets l'angle à 0°
        self.__speed = self.__reset_speed  # Remet les valeurs par défaut de X et Y
        self.__tir = False  # Autorise un nouveau tir
        self.game.coords(self.cible, randrange(700, 1100), randrange(390, 420))  # Déplace aléatoirement la cible

        # Augmente la variable des tirs réussi/ratés
        if resultat: self.__nb_tir[1] += 1  # Ratés
        else: self.__nb_tir[0] += 1  # Réussi

        # Récupère les coordonnées du canon et y colle l'obus
        coords_canon = self.get_coords(self.canon_img, self.canon)
        self.game.coords(self.obus, coords_canon[0]+155, coords_canon[1]+14)

        # Récupère les coordonnées de la barre et la met à zéro
        coords = self.game.coords(self.contenu_anglebar)
        self.game.coords(self.contenu_anglebar, coords[0], 380, coords[2], coords[3])
        self.game.itemconfig(self.contenu_anglebar, fill='darkgreen')

        # Modification des informations pour y ajouter les nouveaux tirs
        succes = self.__nb_tir[0]  # Tirs réussis
        failed = self.__nb_tir[1]  # Tirs ratés
        self.game.itemconfig(self.result, text='Tir{0} réussi{1} : {2}\nTir{3} raté{4} : {5}\nAngle : {6}'.format(Divers.pl(succes), Divers.pl(succes), str(succes), Divers.pl(failed), Divers.pl(failed), str(failed), str(self.__angle)))

    def back_member(self):
        """ Retourne sur l'espace membre """
        self.verif.update(Divers.staticSynthese, int(Divers.staticSynthese[3])+self.__nb_tir[0], int(Divers.staticSynthese[4])+self.__nb_tir[1])  # Mets à jour le classement avec les nouveaux tirs
        self.__nb_tir[0] = 0  # Remet à zéro les tris réussis
        self.__nb_tir[1] = 0  # Remet à zéro les tris ratés
        self.event_generate('<<GAME_LEAVE>>')