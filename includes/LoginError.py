from tkinter import Canvas, Frame, Label, Button, CENTER

from PIL import Image, ImageTk


class LoginError(Frame):
    """Page d'erreur"""

    def __init__(self, windows, **kwargs):
        """ Lancement de l'application """
        super().__init__(windows, **kwargs)
        self.windows = windows
        self._create_interface()

    def _create_interface(self):
        """ Création de l'interface graphique """

        self.bg_frame = Canvas(self.windows, width=1200, height=500, highlightthickness=0)
        self.bg_game = ImageTk.PhotoImage(Image.open('ressources/bg_start.png'))
        self.bg_frame.create_image(0, 0, image=self.bg_game, anchor='nw')
        self.bg_frame.place(x=0, y=0)

        content = Canvas(self.bg_frame, bg='#EDDAC3', width=500, height=75, highlightthickness=0)
        content.place(x=355, y=170)

        content_width = 500
        center_x = content_width // 2

        Label(content, bg='#EDDAC3', text='Vous avez épuisé votre nombre d\'essais, veuillez fermer le programme.',
              fg='darkred', anchor=CENTER, wraplength=450, padx=20, pady=5).place(x=center_x, y=20, anchor=CENTER)

        button_frame = Frame(content, bg='#EDDAC3')
        button_frame.place(x=center_x, y=50, anchor=CENTER)

        quit = Button(button_frame, fg='white', bg='#CA994F', text="Quitter l'application",
                      command=self.windows.destroy)
        quit.grid(row=0, column=0, padx=20, pady=5, ipadx=10, ipady=2)
