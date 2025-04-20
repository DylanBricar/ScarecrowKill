class Utils:
    staticSynthese = []

    def add_plural(nb):
        """ Adds an 's' to words depending on the number """
        if int(nb) > 1: return 's'
        return ''

    def compute_ratio(kill, dead):
        """ Calculates a ratio """
        if int(dead) == 0:
            if int(kill) > 0:

                ratio = round(float(kill), 2)
            else:
                ratio = 0.0
        else:
            ratio = round(int(kill) / int(dead), 2)

        return ratio 