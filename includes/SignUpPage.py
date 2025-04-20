import sys

sys.path.append("includes\\")

from tkinter import Canvas, Frame, Label, Entry, Button, re, END, CENTER
from PIL import Image, ImageTk
from FileVerificator import FileVerificator


class SignUpPage(Frame):
    """ Registration page """

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

        self.content = Canvas(self.bg_frame, width=420, height=220, highlightthickness=0, bg='#EDDAC3')
        self.content.place(x=400, y=170)

        content_width = 420
        center_x = content_width // 2

        self.alert = Label(self.content, bg='#EDDAC3', text='Veuillez remplir les informations pour vous inscrire.',
                           fg='darkblue', anchor=CENTER, wraplength=380, padx=20, pady=5)
        self.alert.place(x=center_x, y=15, anchor=CENTER)

        Label(self.content, bg='#EDDAC3', text='Pseudo', anchor=CENTER, padx=5).place(x=center_x - 105, y=68,
                                                                                      anchor=CENTER)
        self.pseudo = Entry(self.content, highlightthickness=1, justify='left', width=20)
        self.pseudo.place(x=center_x + 40, y=68, anchor=CENTER)

        Label(self.content, bg='#EDDAC3', text='Mot de passe', anchor=CENTER, padx=5).place(x=center_x - 105, y=106,
                                                                                            anchor=CENTER)
        self.password = Entry(self.content, show='*', highlightthickness=1, justify='left', width=20)
        self.password.place(x=center_x + 40, y=106, anchor=CENTER)

        Label(self.content, bg='#EDDAC3', text='Répétez le passe', anchor=CENTER, padx=5).place(x=center_x - 105, y=141,
                                                                                                anchor=CENTER)
        self.password_repeat = Entry(self.content, show='*', highlightthickness=1, justify='left', width=20)
        self.password_repeat.place(x=center_x + 40, y=141, anchor=CENTER)

        button_frame = Frame(self.content, bg='#EDDAC3')
        button_frame.place(x=center_x, y=185, anchor=CENTER)

        submit = Button(button_frame, fg='white', bg='#CA994F', text='S\'inscrire au jeu', command=self.on_signup)
        submit.grid(row=0, column=0, padx=20, pady=5, ipadx=10, ipady=2)

        back = Button(button_frame, fg='white', bg='#CA994F', text='Retour à la page précédente',
                      command=self.on_back)
        back.grid(row=0, column=1, padx=20, pady=5, ipadx=10, ipady=2)

    def on_back(self):
        """ Create an event that redirects to the login page """
        self.event_generate('<<SIGNUP_BACK>>')

    def on_signup(self):
        """ Signup button is pressed, check the data """
        error = []

        if not self.password_repeat.get() or not self.password.get() or not self.pseudo.get():
            error.append('Vous devez remplir tous les champs.')

        if self.password_repeat.get() != self.password.get():
            error.append('Les deux mots de passe ne sont pas identiques.')

        if self.verif.exists_pseudo(self.pseudo.get()):
            error.append('Le nom d\'utilisateur est déjà inscrit.')

        if len(self.password.get()) < 6:
            error.append('Le mot de passe doit être d\'au moins 6 caractères.')

        if len(re.findall('[A-Za-z0-9_-]', self.pseudo.get())) != len(self.pseudo.get()):
            error.append('Le pseudo ne peut pas contenir de caractères spéciaux.')

        if error:
            error_string = '\n'.join(error)
            self.alert['text'] = error_string

            self.password.delete(0, END)
            self.password_repeat.delete(0, END)
        else:
            self.verif.add_line(self.pseudo.get(), self.password.get())
            self.event_generate('<<SIGNUP_SUCCESS>>')
