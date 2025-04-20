import sys

sys.path.append("includes\\")

from datetime import datetime
import hashlib
from Utils import Utils


class FileVerificator:
    def __init__(self):
        """ Loads the content of database.txt into a variable """
        file = open('database.txt', 'r', encoding='utf-8')
        self.lines = file.readlines()
        file.close()

    def exists_pseudo(self, value):
        """ Checks if the search value exists in the file """
        for line in self.lines:

            line_file = (line.replace('\n', '')).split('|')

            if line_file[0].lower() == value.lower():
                return True
                break

    def add_line(self, pseudo, password):
        """ Adds the updated string to the file """

        password_hash = hashlib.sha1(str.encode(password)).hexdigest()
        pattern = str(pseudo) + '|' + password_hash + '|\n'

        file = open('database.txt', 'r', encoding='utf-8')
        old_text = file.read()
        file.close()

        new_file = open('database.txt', 'w', encoding='utf-8')
        new_file.write(old_text + pattern)
        new_file.close()

        file_back = open('database.txt', 'r', encoding='utf-8')
        self.lines = file_back.readlines()
        file_back.close()

        self.validate(pseudo, password)

    def validate(self, pseudo, password):
        """ Validates the username and password """
        for line in self.lines:

            line_file = (line.replace('\n', '')).split('|')

            password_hash = hashlib.sha1(str.encode(password)).hexdigest()

            if line_file[0].lower() == pseudo.lower() and line_file[1] == password_hash:
                self.update(line_file)
                return line_file
                break

    def update(self, line_file, point_win=0, point_lost=0):
        """ Updates and adds information to the synthesis variable """
        Utils.staticSynthese = []
        newlines = []
        new_date = datetime.now().strftime('%d/%m/%Y à %Hh%M')

        for line in self.lines:
            line = (line.replace('\n', ''))

            if line_file[2]:

                search = line_file[0] + '|' + line_file[1] + '|' + line_file[2] + '|' + str(line_file[3]) + '|' + str(
                    line_file[4])
                if point_win == 0: point_win = line_file[3]
                if point_lost == 0: point_lost = line_file[4]

            else:
                search = line_file[0] + '|' + line_file[1] + '|'

            if line in search:
                newlines.append(line_file[0] + '|' + line_file[1] + '|' + new_date + '|' + str(point_win) + '|' + str(
                    point_lost) + '\n')

            else:
                newlines.append(line + '\n')

        with open('database.txt', mode='w', encoding='utf-8') as f:
            f.writelines(newlines)

        Utils.staticSynthese.extend([line_file[0], line_file[1], new_date, point_win, point_lost])

    def classement(self, nb):
        """ Creates a ranking based on ratio """
        all_ratio = []
        classement = []

        for line in self.lines:
            line = (line.replace('\n', '')).split('|')
            all_ratio.append(Utils.compute_ratio(int(line[3]), int(line[4])))

        nb_classement_defaut = len(all_ratio)

        for i in range(1, nb + 1):

            if nb_classement_defaut >= i:
                maximum_ratio = max(all_ratio)

                for line in self.lines:
                    line = (line.replace('\n', '')).split('|')
                    ratio = Utils.compute_ratio(int(line[3]), int(line[4]))

                    if ratio == maximum_ratio:
                        classement.append(
                            str(i) + '. ' + str(line[0]) + ' : ' + line[3] + ' - ' + line[4] + ' => ' + str(
                                ratio) + '\n')
                        all_ratio.remove(ratio)

            else:
                classement.append(str(i) + '. !!! Place libre !!!\n')

        return classement
