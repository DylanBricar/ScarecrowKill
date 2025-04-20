import os
import platform
import sys

includes_path = os.path.join(os.path.dirname(__file__), "includes")
sys.path.append(includes_path)

from tkinter import Tk, CENTER, Frame
import tkinter as tk
from GameCanon import GameCanon
from LoginPage import LoginPage
from MemberPanel import MemberPanel
from LoginError import LoginError
from SignUpPage import SignUpPage


class Controller(Frame):
    """ Redirects the user based on application events """

    def __init__(self, windows, **kwargs):
        """ Application initialization """
        super().__init__(windows, **kwargs)
        self.windows = windows

        self.windows.title('ScarecrowKill')
        self.windows.geometry('1200x500')
        self.windows.resizable(width=False, height=False)

        self._load_favicon()

        self.call_frame = None

        self.place_frame(LoginPage(self.windows), False)

        self._setup_event_bindings()

    def _load_favicon(self):
        """Loads the application icon in an optimized way"""
        favicon_path = os.path.join(os.path.dirname(__file__), 'ressources', 'favicon.ico')
        if os.path.exists(favicon_path):
            self.windows.iconbitmap(favicon_path)

    def _setup_event_bindings(self):
        """Configures all event bindings"""

        events = {
            '<<LOGIN_SUCCES>>': self.is_logged,
            '<<LOGIN_ERROR>>': self.not_logged,
            '<<SIGNUP_PRESS>>': self.pressed_signup,
            '<<SIGNUP_SUCCESS>>': self.is_logged,
            '<<SIGNUP_BACK>>': self.pressed_signup_back,
            '<<GAME_JOIN>>': self.join_game,
            '<<GAME_LEAVE>>': self.is_logged,
            '<<LOGOUT_GAME>>': self.logout
        }

        for event, handler in events.items():
            self.call_frame.bind(event, handler)

    def place_frame(self, page, delete=True):
        """ Places a new frame and optionally destroys the old one """
        if delete and self.call_frame:
            self.call_frame.destroy()

        self.call_frame = page

        self.call_frame.config(bg='#EDDAC3', padx=5000, pady=5000)
        self.call_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def logout(self, event):
        """ Handles user logout """
        self.place_frame(LoginPage(self.windows))
        self._setup_login_bindings()

    def _setup_login_bindings(self):
        """Configures bindings for the login page"""
        login_events = {
            '<<SIGNUP_PRESS>>': self.pressed_signup,
            '<<LOGIN_SUCCES>>': self.is_logged,
            '<<LOGIN_ERROR>>': self.not_logged,
            '<<LOGOUT_GAME>>': self.logout
        }

        for event, handler in login_events.items():
            self.call_frame.bind(event, handler)

    def is_logged(self, event):
        """ Successful user login """
        self.place_frame(MemberPanel(self.windows))

        member_events = {
            '<<GAME_JOIN>>': self.join_game,
            '<<LOGOUT_GAME>>': self.logout
        }

        for event, handler in member_events.items():
            self.call_frame.bind(event, handler)

    def not_logged(self, event):
        """ User has exhausted login attempts """
        self.place_frame(LoginError(self.windows))

    def pressed_signup(self, event):
        """ Signup button was pressed """
        self.place_frame(SignUpPage(self.windows))

        signup_events = {
            '<<SIGNUP_BACK>>': self.pressed_signup_back,
            '<<SIGNUP_SUCCESS>>': self.is_logged
        }

        for event, handler in signup_events.items():
            self.call_frame.bind(event, handler)

    def pressed_signup_back(self, event):
        """ User went back from signup page to login page """
        self.place_frame(LoginPage(self.windows))
        self._setup_login_bindings()

    def join_game(self, event):
        """ Joins the Canon Game """
        self.place_frame(GameCanon(self.windows))

        self.call_frame.bind('<<GAME_LEAVE>>', self.is_logged)


def main():
    """Main entry point of the application"""

    windows = Tk()

    windows.update_idletasks()

    windows.tk_setPalette(background='#EDDAC3')

    if platform.system() == "Darwin":
        try:
            windows.tk.call('::tk::unsupported::MacWindowStyle', 'style', windows._w, 'document', 'closeBox')
        except tk.TclError:
            pass

    controller = Controller(windows)

    windows.mainloop()


if __name__ == "__main__":
    main()
