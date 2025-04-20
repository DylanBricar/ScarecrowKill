import sys

sys.path.append("includes\\")

from tkinter import Canvas, Frame, Label, Entry, Button, END, CENTER
from PIL import Image, ImageTk
from FileVerificator import FileVerificator
from Utils import *


class LoginPage(Frame):
    __trials = 3

    """ Login page """

    def __init__(self, windows, **kwargs):
        """ Initialize the application """
        super().__init__(windows, **kwargs)
        self.windows = windows
        self.verif = FileVerificator()
        self._create_interface()

    def _create_interface(self):
        """ Create the graphical interface """

        self.bg_frame = Canvas(self.windows, width=1200, height=500, highlightthickness=0)
        self.bg_game = ImageTk.PhotoImage(Image.open('ressources/bg_start.png'))
        self.bg_frame.create_image(0, 0, image=self.bg_game, anchor='nw')
        self.bg_frame.place(x=0, y=0)

        self.content = Canvas(self.bg_frame, width=420, height=190, highlightthickness=0, bg='#EDDAC3')
        self.content.place(x=400, y=170)

        content_width = 420
        center_x = content_width // 2

        self.compteur = Label(self.content, bg='#EDDAC3', text=str(self.__trials) + ' essais restants',
                              fg='orange', anchor=CENTER, padx=10)
        self.compteur.place(x=center_x, y=10, anchor=CENTER)

        self.alert = Label(self.content, bg='#EDDAC3',
                           text='Veuillez renseigner vos identifiants pour vous connecter.',
                           fg='darkblue', anchor=CENTER, wraplength=380, padx=20, pady=5)
        self.alert.place(x=center_x, y=35, anchor=CENTER)

        Label(self.content, bg='#EDDAC3', text='Pseudo', anchor=CENTER, padx=5).place(x=center_x - 105, y=75,
                                                                                      anchor=CENTER)
        self.pseudo = Entry(self.content, highlightthickness=1, justify='left', width=20)
        self.pseudo.place(x=center_x + 40, y=75, anchor=CENTER)

        Label(self.content, bg='#EDDAC3', text='Mot de passe', anchor=CENTER, padx=5).place(x=center_x - 105, y=113,
                                                                                            anchor=CENTER)
        self.password = Entry(self.content, show='*', highlightthickness=1, justify='left', width=20)
        self.password.place(x=center_x + 40, y=113, anchor=CENTER)

        button_frame = Frame(self.content, bg='#EDDAC3')
        button_frame.place(x=center_x, y=155, anchor=CENTER)

        submit = Button(button_frame, fg='white', bg='#CA994F', text='Se connecter', command=self.on_login)
        submit.grid(row=0, column=0, padx=20, pady=5, ipadx=10, ipady=2)

        signup = Button(button_frame, fg='white', bg='#CA994F', text='Pas encore de compte ?',
                        command=self.on_click_signup)
        signup.grid(row=0, column=1, padx=20, pady=5, ipadx=10, ipady=2)

    def on_login(self):
        """ Login button pressed, verify credentials """

        if self.verif.validate(self.pseudo.get(), self.password.get()):
            self.event_generate('<<LOGIN_SUCCES>>')

        else:
            self.password.delete(0, END)
            self.__trials -= 1

            if self.__trials > 0:
                self.alert['text'] = 'Les informations insérées sont incorrectes, réessayez.'
                self.compteur['text'] = str(self.__trials) + ' essai' + Utils.add_plural(
                    self.__trials) + " restant" + Utils.add_plural(self.__trials)

            else:

                self.event_generate('<<LOGIN_ERROR>>')

    def on_click_signup(self):
        """ Creates an event that redirects to the registration page when the button is pressed """
        self.event_generate('<<SIGNUP_PRESS>>')
