import sys
sys.path.append("includes\\")

from tkinter import Canvas, Frame, Label, Entry, Button, END
from PIL import Image, ImageTk
from FileVerificator import FileVerificator
from Divers import *

# ----------------------------------------------------------------
# -------------- PAGE DE CONNEXION
# ----------------------------------------------------------------


class LoginPage(Frame):
    __trials = 3  # Nombre d'essais maximum de connexion

    """ Page de connexion """
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

        # Crée le conteneur des informations
        self.content = Canvas(self.bg_frame, width=420, height=190)
        self.content.place(x=400, y=170)

        # Crée le compteur d'essais
        self.compteur = Label(self.content, bg='white', text=str(self.__trials) + ' essais restants', fg='orange')
        self.compteur.place(x=155, y=10)

        # Affiche l'alerte
        self.alert = Label(self.content, bg='white', text='Veuillez renseigner vos identifiants pour vous connecter.', fg='darkblue')
        self.alert.place(x=30, y=35)

        # Crée la légende et le champ du pseudo
        Label(self.content, bg='white', text='Pseudo').place(x=60, y=75)
        self.pseudo = Entry(self.content)
        self.pseudo.place(x=165, y=72)

        # Crée la légende et le champ du mot de passe
        Label(self.content, bg='white', text='Mot de passe').place(x=60, y=113)
        self.password = Entry(self.content, show='*')
        self.password.place(x=165, y=110)

        # Affiche le bouton pour envoyer les données
        submit = Button(self.content, fg='white', bg='#CA994F', text='Se connecter', command=self.on_login)
        submit.grid(ipadx=10, ipady=2)
        submit.place(x=50, y=155)

        # Affiche le bouton pour envoyer créer un compte
        signup = Button(self.content, fg='white', bg='#CA994F', text='Pas encore de compte ?', command=self.on_clickSignup)
        signup.grid(ipadx=10, ipady=2)
        signup.place(x=190, y=155)

    def on_login(self):
        """ Bouton de connexion pressé, il faut vérifier les données """
        # Le pseudo et le mot de passe correspondent
        if self.verif.validate(self.pseudo.get(), self.password.get()):
            self.event_generate('<<LOGIN_SUCCES>>')  # Crée un evenement pour afficher la page de membre
        # Si les données sont incorrectes
        else:
            self.password.delete(0, END)  # Supprime le mot de passe pré-rempli
            self.__trials -= 1  # Retire 1 essai

            # S'il y a encore des essais restants
            if self.__trials > 0:
                self.alert['text'] = 'Les informations insérées sont incorrectes, réessayez.'
                self.compteur['text'] = str(self.__trials) + ' essai' + Divers.pl(self.__trials) + " restant" + Divers.pl(self.__trials)
            # Plus aucun essais restants
            else:
                # Crée un evenement qui redirige vers la page d'echec de connexion
                self.event_generate('<<LOGIN_ERROR>>')

    def on_clickSignup(self):
        """ Crée un événement qui redirige vers la page d'inscription car le bouton est pressé """
        self.event_generate('<<SIGNUP_PRESS>>')
