import sys
sys.path.append("includes\\")

from tkinter import Canvas, Frame, Label, Entry, Button, re, END
from PIL import Image, ImageTk
from FileVerificator import FileVerificator

# ----------------------------------------------------------------
# -------------- PAGE D'INSCRIPTION
# ----------------------------------------------------------------


class SignUpPage(Frame):
    """ Page d'inscription """
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
        self.content = Canvas(self.bg_frame, width=420, height=220)
        self.content.place(x=400, y=170)

        # Affiche l'alerte
        self.alert = Label(self.content, bg='white', text='Veuillez remplir les informations pour vous inscrire.', fg='darkblue')
        self.alert.place(x=40, y=10)

        # Crée la légende et le champ du pseudo
        Label(self.content, bg='white', text='Pseudo').place(x=55, y=68)
        self.pseudo = Entry(self.content)
        self.pseudo.place(x=180, y=65)

        # Crée la légende et le champ du mot de passe
        Label(self.content, bg='white', text='Mot de passe').place(x=55, y=106)
        self.password = Entry(self.content, show='*')
        self.password.place(x=180, y=102)

        # Crée la légende et le champ du mot de passe répété
        Label(self.content, bg='white', text='Répétez le passe').place(x=55, y=141)
        self.password_repeat = Entry(self.content, show='*')
        self.password_repeat.place(x=180, y=138)

        # Affiche le bouton pour envoyer les données
        submit = Button(self.content, fg='white', bg='#CA994F', text='S\'inscrire au jeu', command=self.on_signup)
        submit.grid(ipadx=10, ipady=2)
        submit.place(x=40, y=185)

        # Affiche le bouton pour revenir en arrière
        back = Button(self.content, fg='white', bg='#CA994F', text='Retour à la page précédente', command=self.back_page)
        back.grid(ipadx=10, ipady=2)
        back.place(x=180, y=185)

    def back_page(self):
        """ Retourne sur la page de connexion """
        self.event_generate('<<SIGNUP_BACK>>')

    def on_signup(self):
        """ Bouton d'inscription pressé, il faut vérifier les données """
        error = []  # Liste vide pour les erreurs

        # Tous les champs ne sont pas remplis
        if not self.password_repeat.get() or not self.password.get() or not self.password_repeat.get():
            error.append('Vous devez remplir tous les champs.')

        # Les deux mots de passe ne sont pas identiques
        if self.password_repeat.get() != self.password.get():
            error.append('Les deux mots de passe ne sont pas identiques.')

        # Le pseudo est déjà enregistré
        if self.verif.existPseudo(self.pseudo.get()):
            error.append('Le nom d\'utilisateur est déjà inscrit.')

        # La longeur du mot de passe est inférieure à 6 caractères
        if len(self.password.get()) < 6:
            error.append('Le mot de passe doit être d\'au moins 6 caractères.')

        # Vérifie la différence de taille des pseudos avec et sans les caractères spéciaux
        if len(re.findall('[A-Za-z0-9_-]', self.pseudo.get())) != len(self.pseudo.get()):
            error.append('Le pseudo ne peut pas contenir de caractères spéciaux.')

        if error:  # S'il y a des erreurs
            error_string = '\n'.join(error)  # Explose la liste pour le convertir en chaine de caractère
            self.alert['text'] = error_string  # Ajoute les erreurs au tableau

            # Supprime les mots de passe envoyés dans le formulaire
            self.password.delete(0, END)
            self.password_repeat.delete(0, END)
        else:  # S'il n'y a pas d'erreur
            # Crée une nouvelle ligne dans le fichier et retourne l'événement pour la page de membre
            self.verif.addLine(self.pseudo.get(), self.password.get())
            self.event_generate('<<SIGNUP_SUCCESS>>')
