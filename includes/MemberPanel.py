import sys

sys.path.append("includes\\")

from tkinter import Canvas, Frame, Label, Button, LEFT, CENTER, Text, FLAT, font
from PIL import Image, ImageTk
from Utils import Utils
from FileVerificator import FileVerificator


class MemberPanel(Frame):
    """ Member panel page """

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

        text_classement = self.verif.classement(5)
        ratio = Utils.compute_ratio(Utils.staticSynthese[3], Utils.staticSynthese[4])

        screen_center_x = 600
        left_panel_x = screen_center_x - 140
        right_panel_x = screen_center_x + 210

        header_y = 170
        content_y = 300
        footer_y = 420

        canv_bienvenue_width = 770
        canv_bienvenue_height = 50
        canv_bienvenue = Canvas(self.bg_frame, width=canv_bienvenue_width, height=canv_bienvenue_height,
                                highlightthickness=0, bg='#EDDAC3')
        canv_bienvenue.place(x=screen_center_x, y=header_y, anchor=CENTER)

        canv_info_width = 470
        canv_info_height = 150
        canv_info = Canvas(self.bg_frame, width=canv_info_width, height=canv_info_height, highlightthickness=0,
                           bg='#EDDAC3')
        canv_info.place(x=left_panel_x, y=content_y, anchor=CENTER)

        canv_classement_width = 280
        canv_classement_height = canv_info_height
        canv_classement = Canvas(self.bg_frame, width=canv_classement_width, height=canv_classement_height,
                                 highlightthickness=0, bg='#EDDAC3')
        canv_classement.place(x=right_panel_x, y=content_y, anchor=CENTER)

        canv_buttons_width = 770
        canv_buttons_height = 50
        canv_buttons = Canvas(self.bg_frame, width=canv_buttons_width, height=canv_buttons_height, highlightthickness=0,
                              bg='#EDDAC3')
        canv_buttons.place(x=screen_center_x, y=footer_y, anchor=CENTER)

        bienvenue = Label(canv_bienvenue, bg='#EDDAC3', fg='#EEAD0E', font=('Helvetica', 20, 'bold'),
                          text='Bienvenue dans ton espace membre ' + str(Utils.staticSynthese[0].capitalize()) + ' !',
                          anchor=CENTER, padx=30, pady=10)
        bienvenue.place(x=canv_bienvenue_width // 2, y=canv_bienvenue_height // 2, anchor=CENTER)

        Label(canv_info, fg='#CD5B45', bg='#EDDAC3', font=('Helvetica', 18, 'bold'), text='Informations :',
              anchor=CENTER, padx=10).place(x=canv_info_width // 2, y=20, anchor=CENTER)

        successful_shots = Utils.staticSynthese[3]
        failed_shots = Utils.staticSynthese[4]
        
        info_text = (
            'Dernière connexion : le ' + str(Utils.staticSynthese[2]) + '.\n' +
            'Vous avez accumulé un total de ' + str(successful_shots) + ' tir' + 
            Utils.add_plural(successful_shots) + ' gagnant' + Utils.add_plural(successful_shots) + '.\n' +
            'Vous avez accumulé un total de ' + str(failed_shots) + ' tir' + 
            Utils.add_plural(failed_shots) + ' perdant' + Utils.add_plural(failed_shots) + '.\n' +
            'Votre ratio de tirs réussis/ratés s\'élève à ' + str(ratio) + '.'
        )

        info = Label(canv_info, justify=LEFT, bg='#EDDAC3', text=info_text,
                     wraplength=canv_info_width - 40, padx=20, pady=5)
        info.place(x=canv_info_width // 2, y=85, anchor=CENTER)

        Label(canv_classement, fg='#CD5B45', bg='#EDDAC3', font=('Helvetica', 18, 'bold'), text='Classement :',
              anchor=CENTER, padx=10).place(x=canv_classement_width // 2, y=20, anchor=CENTER)

        default_font = font.nametofont("TkDefaultFont")

        classement_text = Text(canv_classement, bg='#EDDAC3', bd=0, highlightthickness=0, relief=FLAT,
                               height=6, width=32, font=default_font, padx=20, pady=5)
        classement_text.place(x=15, y=45)

        classement_text.insert("1.0", "#")

        for item in text_classement:
            classement_text.insert("end", item)

        classement_text.config(state="disabled")

        button_frame = Frame(canv_buttons, bg='#EDDAC3')
        button_frame.place(x=canv_buttons_width // 2, y=canv_buttons_height // 2, anchor=CENTER)

        play = Button(button_frame, fg='white', bg='#CA994F', text='Lancer le jeu', command=self.game_join)
        play.grid(row=0, column=0, padx=25, pady=10, ipadx=15, ipady=5)

        logout = Button(button_frame, fg='white', bg='#CA994F', text='Se déconnecter', command=self.game_disconnect)
        logout.grid(row=0, column=1, padx=25, pady=10, ipadx=15, ipady=5)

        quit = Button(button_frame, fg='white', bg='#CA994F', text='Fermer la fenêtre', command=self.windows.destroy)
        quit.grid(row=0, column=2, padx=25, pady=10, ipadx=15, ipady=5)

    def game_join(self):
        """ Event to open the game window """
        self.event_generate('<<GAME_JOIN>>')

    def game_disconnect(self):
        """ Event to disconnect from the game """
        self.event_generate('<<LOGOUT_GAME>>')
