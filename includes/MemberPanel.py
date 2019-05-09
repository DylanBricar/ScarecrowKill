import sys
sys.path.append("includes\\")

from tkinter import Canvas, Frame, Label, Button, LEFT
from PIL import Image, ImageTk
from Divers import Divers
from FileVerificator import FileVerificator

# ----------------------------------------------------------------
# -------------- PAGE DE MEMBRE
# ----------------------------------------------------------------


class MemberPanel(Frame):
    """ Page de membre """
    def __init__(self, windows, **kwargs):
        """ Lancement de l'application """
        super().__init__(windows, **kwargs)  # Permet de récupérer les précédents arguments appelés
        self.windows = windows  # Rend la fenêtre importée globale à toute la class
        self.verif = FileVerificator()  # Instancie la includes de vérification des fichiers
        self._create_interface()  # Crée l'interface pour s'inscrire à l'application

    def _create_interface(self):
        """ Création de l'interface graphique """
        # Crée le canvas avec le fond et collé au bord de la fenêtre
        self.bg_frame = Canvas(self.windows, width=1200, height=500, highlightthickness=0)
        self.bg_game = ImageTk.PhotoImage(Image.open('ressources/bg_start.png'))
        self.bg_frame.create_image(0, 0, image=self.bg_game, anchor='nw')
        self.bg_frame.place(x=0, y=0)

        text_classement = ''.join(self.verif.classement(5))
        ratio = Divers.ratio(Divers.staticSynthese[3], Divers.staticSynthese[4])

        # Crée le conteneur du message de bienvenue
        canv_bienvenue = Canvas(self.bg_frame, width=770, height=30)
        canv_bienvenue.place(x=230, y=170)

        # Crée le conteneur des informations personnelles
        canv_info = Canvas(self.bg_frame, width=470, height=150)
        canv_info.place(x=230, y=220)

        # Crée le conteneur du classement
        canv_classement = Canvas(self.bg_frame, width=280, height=150)
        canv_classement.place(x=720, y=220)

        # Crée le conteneur des boutons
        canv_buttons = Canvas(self.bg_frame, width=770, height=30)
        canv_buttons.place(x=230, y=390)

        # Affiche le message de bienvenue avec la premiÃƒÂ¨re lettre du pseudo en majuscule
        bienvenue = Label(canv_bienvenue, bg='white', fg='#EEAD0E', font=('Helvetica', 20, 'bold'), text='Bienvenue dans ton espace membre ' + str(Divers.staticSynthese[0].capitalize()) + ' !')
        bienvenue.place(x=170, y=5)

        # Affiche le titre des informations personnelles
        Label(canv_info, fg='#CD5B45', bg='white', font=('Helvetica', 18, 'bold'), text='Informations :').place(x=170, y=10)
        # Affiche toutes les informations personnelles
        info = Label(canv_info, justify=LEFT, text='DerniÃƒÂ¨re connexion : le ' + str(Divers.staticSynthese[2]) + '.\nVous avez accumulé un total de ' + str(Divers.staticSynthese[3]) + ' tir' + Divers.pl(Divers.staticSynthese[3]) + ' gagnant' + Divers.pl(Divers.staticSynthese[3]) + '.\nVous avez accumulé un total de ' + str(Divers.staticSynthese[4]) + ' tir' + Divers.pl(Divers.staticSynthese[4]) + ' perdant' + Divers.pl(Divers.staticSynthese[4])+'.\nVotre ratio de tirs réussis/ratés s\'élÃƒÂ¨ve à ' + str(ratio) + '.')
        info.place(x=10, y=40)

        # Affiche le titre du classement
        Label(canv_classement, fg='#CD5B45', bg='white', font=('Helvetica', 18, 'bold'), text='Classement :').place(x=80, y=10)
        # Affiche la légende pour le classement
        Label(canv_classement, justify=LEFT, text='## Pseudo : réussis | ratés => ratio').place(x=10, y=40)
        # Affiche toutes les informations du classement
        classement = Label(canv_classement, bg='white', justify=LEFT, text=text_classement)
        classement.place(x=10, y=60)

        # Affiche le bouton pour lancer le jeu
        play = Button(canv_buttons, fg='white', bg='#CA994F', text='Lancer le jeu', command=self.game_join)
        play.grid(ipadx=10, ipady=2)
        play.place(x=10, y=4)

        # Affiche le bouton pour se déconnecter de l'application
        logout = Button(canv_buttons, fg='white', bg='#CA994F', text='Se déconnecter', command=self.game_disconnect)
        logout.grid(ipadx=10, ipady=2)
        logout.place(x=310, y=4)

        # Affiche le bouton pour quitter l'application
        quit = Button(canv_buttons, fg='white', bg='#CA994F', text='Fermer la fenêtre', command=self.windows.destroy)
        quit.grid(ipadx=10, ipady=2)
        quit.place(x=630, y=4)

    def game_join(self):
        """ Evenement pour ouvrir la fenêtre du jeu """
        self.event_generate('<<GAME_JOIN>>')

    def game_disconnect(self):
        """ Evenement pour se déconnecter du jeu """
        self.event_generate('<<LOGOUT_GAME>>')