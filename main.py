import sys
sys.path.append("includes\\")

from tkinter import Tk, CENTER, Frame
from GameCanon import GameCanon
from LoginPage import LoginPage
from MemberPanel import MemberPanel
from LoginError import LoginError
from SignUpPage import SignUpPage


# ----------------------------------------------------------------
# -------------- GESTION DU CONTROLLER
# ----------------------------------------------------------------

class Controller(Frame):
    """ Redirige l'utilisateur en fonction des événements apportés """
    def __init__(self, windows, **kwargs):
        """ Lancement de l'application """
        super().__init__(windows, **kwargs)  # Permet de récupérer les précédents arguments appelés
        self.windows = windows  # Rend la fenêtre importée globale à toute la class

        # Configurations de la fenêtre
        self.windows = windows
        windows.title('ScarecrowKill')
        windows.geometry('1200x500')
        windows.resizable(width=False, height=False)
        windows.iconbitmap('ressources/favicon.ico')

        # Affiche la fenêtre de connexion et demande de ne pas vider la fenêtre précédente
        self.placeFrame(LoginPage(self.windows), False)

        # Execute une fonction par rapport à l'évenement récupéré
        self.call_frame.bind('<<LOGIN_SUCCES>>', self.is_logged)
        self.call_frame.bind('<<LOGIN_ERROR>>', self.not_logged)
        self.call_frame.bind('<<SIGNUP_PRESS>>', self.pressed_signup)
        self.call_frame.bind('<<SIGNUP_SUCCESS>>', self.is_logged)
        self.call_frame.bind('<<SIGNUP_BACK>>', self.pressed_signup_back)
        self.call_frame.bind('<<GAME_JOIN>>', self.join_game)
        self.call_frame.bind('<<GAME_LEAVE>>', self.is_logged)
        self.call_frame.bind('<<LOGOUT_GAME>>', self.logout)

    def placeFrame(self, page, delete=True):
        """ Permet de placer la nouvelle fenêtre et de détruire ou pas l'ancienne """
        if delete: self.call_frame.destroy()  # Détruit la page précédente si la variable delete est sur True
        self.call_frame = page  # Dirige vers la nouvelle page appelée
        self.call_frame.config(bg='#EDDAC3', padx=5000, pady=5000)
        self.call_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def logout(self, event):
        """ La connexion à l'utilisateur est réussie """
        self.placeFrame(LoginPage(self.windows))
        # Dirige vers la fonction prévue si celle-ci est appellée dans la page de connexion
        self.call_frame.bind('<<SIGNUP_PRESS>>', self.pressed_signup)
        self.call_frame.bind('<<LOGIN_SUCCES>>', self.is_logged)
        self.call_frame.bind('<<LOGIN_ERROR>>', self.not_logged)
        self.call_frame.bind('<<LOGOUT_GAME>>', self.logout)

    def is_logged(self, event):
        """ La connexion à l'utilisateur est réussie """
        self.placeFrame(MemberPanel(self.windows))
        # Dirige vers la fonction du jeu si celle-ci est appellée dans la page membre
        self.call_frame.bind('<<GAME_JOIN>>', self.join_game)
        # Dirige vers la fonction de déconnexion si celle-ci est appellée dans la page membre
        self.call_frame.bind('<<LOGOUT_GAME>>', self.logout)

    def not_logged(self, event):
        """ L'utilisateur a épuisé ses essais de connexion """
        self.placeFrame(LoginError(self.windows))

    def pressed_signup(self, event):
        """ Le bouton pour s'inscrire est pressé """
        self.placeFrame(SignUpPage(self.windows))
        # Dirige vers la fonction prévue si celle-ci est appellée dans la page d'inscription
        self.call_frame.bind('<<SIGNUP_BACK>>', self.pressed_signup_back)
        self.call_frame.bind('<<SIGNUP_SUCCESS>>', self.is_logged)

    def pressed_signup_back(self, event):
        """ L'utilisateur est retourné de la page d'inscription à connexion """
        self.placeFrame(LoginPage(self.windows))
        # Dirige vers la fonction prévue si celle-ci est appellée dans la page de connexion
        self.call_frame.bind('<<SIGNUP_PRESS>>', self.pressed_signup)
        self.call_frame.bind('<<LOGIN_SUCCES>>', self.is_logged)
        self.call_frame.bind('<<LOGIN_ERROR>>', self.not_logged)

    def join_game(self, event):
        """ Rejoint le jeu du Canon """
        self.placeFrame(GameCanon(self.windows))
        # Dirige l'utilisateur vers la page de membre s'il quitte le jeu
        self.call_frame.bind('<<GAME_LEAVE>>', self.is_logged)


# Défini et lance l'application TKinter
windows = Tk()
controller = Controller(windows)
windows.mainloop()