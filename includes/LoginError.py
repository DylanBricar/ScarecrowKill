from tkinter import Canvas, Frame, Label, Button
from PIL import Image, ImageTk

# ----------------------------------------------------------------
# -------------- MAXIMUM D'ESSAIS DE CONNEXION
# ----------------------------------------------------------------


class LoginError(Frame):
    """Page d'erreur"""
    def __init__(self, windows, **kwargs):
        """ Lancement de l'application """
        super().__init__(windows, **kwargs)  # Permet de rÃ©cupÃ©rer les prÃ©cÃ©dents arguments appelÃ©s
        self.windows = windows  # Rend la fenêtre importÃ©e globale Ã  toute la class
        self._create_interface()  # CrÃ©e l'interface pour quitter l'application

    def _create_interface(self):
        """ CrÃ©ation de l'interface graphique """
        # CrÃ©e le canvas avec le fond et collÃ© au bord de la fenêtre
        self.bg_frame = Canvas(self.windows, width=1200, height=500, highlightthickness=0)
        self.bg_game = ImageTk.PhotoImage(Image.open('ressources/bg_start.png'))
        self.bg_frame.create_image(0, 0, image=self.bg_game, anchor='nw')
        self.bg_frame.place(x=0, y=0)

        # CrÃ©e le conteneur des informations
        content = Canvas(self.bg_frame, bg='white', width=500, height=75)
        content.place(x=355, y=170)

        # Affiche l'alerte
        Label(content, bg='white', text='Vous avez Ã©puisez votre nombre d\'essais, veuillez fermer le programme.', fg='darkred').place(x=18, y=10)

        # Affiche le bouton pour quitter
        quit = Button(content, fg='white', bg='#CA994F', text="Quitter l'application", command=self.windows.destroy)
        quit.grid(ipadx=10, ipady=2)
        quit.place(x=178, y=40)
