import sys

sys.path.append("includes\\")

from tkinter import Canvas, Frame, Button, PhotoImage, NW
from PIL import Image, ImageTk
from random import randrange
from math import pi, sin, cos
from functools import lru_cache
from FileVerificator import FileVerificator
from Utils import Utils


class GameCanon(Frame):
    __ANGLE_MAX = 80
    __ANGLE_MIN = 0
    __ANGLE_STEP = 2
    __ANGLE_BAR_STEP = 7

    __angle = 0
    __x_deplace = 15
    __dt = 20
    __g = 50
    __tir = False
    __nb_tir = [0, 0]
    __list_speed = [30, -20]
    __speed = [__list_speed[0], __list_speed[1] * 0]
    __reset_speed = [__list_speed[0], __list_speed[1] * 0]

    __init_obus_x = 176
    __init_obus_y = 400

    __cached_images = {}

    def __init__(self, windows, **kwargs):
        """ Initialize the application """
        super().__init__(windows, **kwargs)
        self.windows = windows
        self.verif = FileVerificator()
        self._create_interface()

    @staticmethod
    @lru_cache(maxsize=8)
    def _load_image(path):
        """Loads an image with caching"""
        if path.endswith('.gif'):
            return PhotoImage(file=path)
        return ImageTk.PhotoImage(Image.open(path))

    def _create_interface(self):
        """ Create the graphical interface """

        self.game = Canvas(self.windows, width=1200, height=500, highlightthickness=0)
        self.bg_game = self._load_image('ressources/bg_game.png')
        self.game.create_image(0, 0, image=self.bg_game, anchor='nw')
        self.game.place(x=0, y=0)

        self.roues_img = self._load_image('ressources/roues.gif')
        self.roues = self.game.create_image(90, 467, image=self.roues_img)

        self.canon_img = self._load_image('ressources/canon.gif')
        self.canon = self.game.create_image(100, 440, image=self.canon_img)

        self.cible_img = self._load_image('ressources/cible.gif')
        self.cible = self.game.create_image(randrange(700, 1100), randrange(390, 420), image=self.cible_img)

        self.obus_img = self._load_image('ressources/obus.gif')
        self.obus = self.game.create_image(self.__init_obus_x, self.__init_obus_y, image=self.obus_img)

        self._precalculate_image_dimensions()

        result_rect = self.game.create_rectangle(10, 10, 250, 120, fill='white')
        info = self.game.create_text(130, 28, fill='darkred', font=('Helvetica', 20, 'bold'), text='Informations', )
        self.result = self.game.create_text(75, 79, font=('Helvetica', 14),
                                            text='Tir réussi : {0}\nTir raté : {1}\nAngle : {2}'.format(
                                                str(self.__nb_tir[0]), str(self.__nb_tir[1]), str(abs(self.__angle))))

        fond_anglebar = self.game.create_rectangle(1170, 89, 1190, 400, fill='white')
        self.contenu_anglebar = self.game.create_rectangle(1175, 380, 1185, 390, fill='darkgreen')

        self.game.tag_raise(info, result_rect)
        self.game.tag_raise(self.result, result_rect)
        self.game.tag_raise(self.contenu_anglebar, fond_anglebar)

        btn_quitter = Button(self.windows, fg='white', bg='#CA994F', text='Revenir à l\'espace membre',
                             command=self.back_member)
        btn_quitter.grid(ipadx=10, ipady=2)
        self.game.create_window(998, 10, anchor=NW, window=btn_quitter)

        self._setup_key_bindings()

    def _precalculate_image_dimensions(self):
        """Pre-calculates image dimensions to avoid recalculating on each frame"""
        self.obus_halfwidth = self.obus_img.width() / 2
        self.obus_halfheight = self.obus_img.height() / 2
        self.cible_halfwidth = self.cible_img.width() / 2
        self.cible_halfheight = self.cible_img.height() / 2
        self.canon_halfwidth = self.canon_img.width() / 2
        self.canon_halfheight = self.canon_img.height() / 2

    def _setup_key_bindings(self):
        """Configure key bindings"""
        key_bindings = {
            '<space>': self._handle_space,
            '<Up>': lambda event: self._handle_angle('Up'),
            '<Down>': lambda event: self._handle_angle('Down'),
            '<Left>': lambda event: self._handle_movement('Left'),
            '<Right>': lambda event: self._handle_movement('Right')
        }

        for key, handler in key_bindings.items():
            self.windows.bind(key, handler)

    def _handle_space(self, event):
        """Handles spacebar key press (shooting)"""
        if not self.__tir:
            self.shoot()

    def _handle_angle(self, direction):
        """Handles angle changes"""
        if not self.__tir:
            self.set_angle(direction)

    def _handle_movement(self, direction):
        """Handles cannon movement"""
        if not self.__tir:
            self.move(direction)

    def router(self, event):
        """ Reacts based on the received event """

        if event.keysym == 'space' and not self.__tir:
            self.shoot()
        elif (event.keysym == 'Up' or event.keysym == 'Down') and not self.__tir:
            self.set_angle(event.keysym)
        elif (event.keysym == 'Left' or event.keysym == 'Right') and not self.__tir:
            self.move(event.keysym)

    def set_angle(self, touche):
        """ Sets the firing angle of the cannon and modifies the angle bar """

        coords = self.game.coords(self.contenu_anglebar)
        new_y_anglebar = coords[1]

        if self.__angle >= self.__ANGLE_MAX:
            if touche == 'Down':
                self.__angle -= self.__ANGLE_STEP
                new_y_anglebar = coords[1] + self.__ANGLE_BAR_STEP
        elif self.__angle <= self.__ANGLE_MIN:
            if touche == 'Up':
                self.__angle += self.__ANGLE_STEP
                new_y_anglebar = coords[1] - self.__ANGLE_BAR_STEP
        else:
            if touche == 'Up':
                self.__angle += self.__ANGLE_STEP
                new_y_anglebar = coords[1] - self.__ANGLE_BAR_STEP
            if touche == 'Down':
                self.__angle -= self.__ANGLE_STEP
                new_y_anglebar = coords[1] + self.__ANGLE_BAR_STEP

        self._update_result_text()

        angle_rad = float(self.__angle) * 2 * pi / 360
        self.__speed = [
            self.__list_speed[0] * cos(angle_rad),
            self.__list_speed[1] * sin(angle_rad)
        ]

        self.game.coords(self.contenu_anglebar, coords[0], new_y_anglebar, coords[2], coords[3])
        self._update_angle_bar_color()

    def _update_result_text(self):
        """Updates the result text"""
        succes = self.__nb_tir[0]
        failed = self.__nb_tir[1]
        self.game.itemconfig(
            self.result,
            text=f'Tir{Utils.add_plural(succes)} réussi{Utils.add_plural(succes)} : {succes}\n'
                 f'Tir{Utils.add_plural(failed)} raté{Utils.add_plural(failed)} : {failed}\n'
                 f'Angle : {abs(self.__angle)}'
        )

    def _update_angle_bar_color(self):
        """Updates the angle bar color based on the current angle"""
        color = 'darkgreen'

        if self.__angle > 70:
            color = 'darkred'
        elif self.__angle > 50:
            color = 'red'
        elif self.__angle > 30:
            color = 'orange'

        self.game.itemconfig(self.contenu_anglebar, fill=color)

    def move(self, touche):
        """ Horizontally moves the cannon, wheels and attached shell """

        coords_obus = self.game.coords(self.obus)
        x_obus = coords_obus[0]

        if touche == 'Right' and x_obus < 400:
            delta = self.__x_deplace

        elif touche == 'Left' and x_obus > 170:
            delta = -self.__x_deplace
        else:
            return

        self.game.move(self.obus, delta, 0)
        self.game.move(self.roues, delta, 0)
        self.game.move(self.canon, delta, 0)

    def shoot(self):
        """ Fires the shell """

        if self.__speed != [0, 0]:

            if not self.is_impacted():
                self.reset(False)
                return

            self.__speed = self.move_img(self.obus_img, self.obus, self.__speed)
            self.game.move(self.obus, self.__speed[0], self.__speed[1])

            self.game.after(self.__dt, self.shoot)
            self.__tir = True
        else:
            self.reset(True)

    def get_coords(self, img, obj):
        """ Gets the coordinates of an image object """

        if img == self.obus_img:
            halfwidth = self.obus_halfwidth
            halfheight = self.obus_halfheight
        elif img == self.cible_img:
            halfwidth = self.cible_halfwidth
            halfheight = self.cible_halfheight
        elif img == self.canon_img:
            halfwidth = self.canon_halfwidth
            halfheight = self.canon_halfheight
        else:

            halfwidth = img.width() / 2
            halfheight = img.height() / 2

        centre = self.game.coords(obj)

        return [centre[0] - halfwidth, centre[1] - halfheight, centre[0] + halfwidth, centre[1] + halfheight]

    def move_img(self, image, obj, speed):
        """ Moves an object by a given speed vector """
        coordonnees = self.get_coords(image, obj)

        if (coordonnees[0] <= 0) or (coordonnees[2] >= 1200 - speed[0]):
            return [0, 0]

        if (coordonnees[1] <= 0) or (coordonnees[3] >= 500 - speed[1]):
            return [0, 0]

        new_speed_y = speed[1] + int(self.__g * self.__dt / 1000)
        return [speed[0], new_speed_y]

    def is_impacted(self):
        """ Checks if the shell has hit the target """

        coords_obus = self.game.coords(self.obus)
        coords_cible = self.game.coords(self.cible)

        dx = abs(coords_obus[0] - coords_cible[0])
        dy = abs(coords_obus[1] - coords_cible[1])

        if dx > self.obus_halfwidth + self.cible_halfwidth or dy > self.obus_halfheight + self.cible_halfheight:
            return True

        if (coords_cible[0] - self.cible_halfwidth <= coords_obus[0] - self.obus_halfwidth <= coords_cible[
            0] + self.cible_halfwidth) and \
                (coords_cible[1] - self.cible_halfheight <= coords_obus[1] - self.obus_halfheight <= coords_cible[
                    1] + self.cible_halfheight):
            return False

        return True

    def reset(self, resultat):
        """ Resets the game after a shot """
        self.__angle = 0
        self.__speed = self.__reset_speed.copy()
        self.__tir = False

        new_x = randrange(700, 1100)
        new_y = randrange(390, 420)
        self.game.coords(self.cible, new_x, new_y)

        if resultat:
            self.__nb_tir[1] += 1
        else:
            self.__nb_tir[0] += 1

        coords_canon = self.game.coords(self.canon)
        self._position_obus_at_canon(coords_canon)

        coords = self.game.coords(self.contenu_anglebar)
        self.game.coords(self.contenu_anglebar, coords[0], 380, coords[2], coords[3])
        self.game.itemconfig(self.contenu_anglebar, fill='darkgreen')

        self._update_result_text()

    def _position_obus_at_canon(self, coords_canon):
        """ Positions the shell at the cannon """

        x_obus = coords_canon[0] + 76
        y_obus = coords_canon[1] - 40

        self.game.coords(self.obus, x_obus, y_obus)

    def back_member(self):
        """ Returns to the member panel """

        self.verif.update(
            Utils.staticSynthese,
            int(Utils.staticSynthese[3]) + self.__nb_tir[0],
            int(Utils.staticSynthese[4]) + self.__nb_tir[1]
        )

        self.__nb_tir = [0, 0]

        self.event_generate('<<GAME_LEAVE>>')
