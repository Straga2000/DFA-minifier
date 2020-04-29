from CONSTANTS_AND_LIBRARIES import *

class Reader:
    def __init__(self, point, length):

        self.entry = Entry(point, length)

    def get_input(self):

        return self.entry.getText()

    def set_text(self, text):

        return self.entry.setText(text)

    def print_reader(self, win):

        return self.entry.draw(win)

    def read_word(self, win):

        # citirea cuvantului
        if win.getMouse():

            line = self.get_input()
            self.set_text("")

            if line == "*":
                win.close()
                return False

            if line == "":
                return None

            elif line == line.split()[0]:
                # daca "cuvantul"(din limbajul automatului) e dat caracter cu caracter (sau daca e dat cuvant cu cuvant)
                word = list(line)

            else:
                word = line.split()

            return word

class WindowObject:
    def __init__(self, name, width, height):

        self.width = width
        self.height = height
        self.win = GraphWin(name, width, height)
        self.win.setBackground(bg_color)

        self.infoText = Text(Point(self.width / 2, self.height - 30), "")
        self.infoText.setTextColor(white)
        self.infoText.setSize(15)

        self.entry = Reader(Point(self.width / 2, 30), 20)
        self.entry.print_reader(self.win)

    def print_message(self, text):
        self.infoText.undraw()
        self.infoText.setText(text)
        self.infoText.draw(self.win)

    def unprint_message(self):
        self.infoText.undraw()

    def read_word(self):
        return self.entry.read_word(self.win)

    def mouse_click(self):
        return self.win.getMouse()

