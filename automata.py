from graphics import *
from random import randint
from math import atan, sin, cos, pi

white = color_rgb(255, 255, 255)
red = color_rgb(255, 0, 0)
green = color_rgb(124, 252, 0)
yellow = color_rgb(247, 239, 1)
bg_color = color_rgb(50, 50, 50)

stateList = {"start": 1, "end": -1}

class Node:

    def __init__(self, text, radius, point=Point(200, 200)):

        self.state = []

        self.circle = Circle(point, radius)

        self.text = Text(point, text)

        self.color = None

        self.arrowList = {}

        self.isPrinted = False

    def rewrite(self, point, window):
        if self.isPrinted is True:
            self.unprint()

        if self.isPrinted is False:
            self.circle = Circle(point, self.circle.getRadius())
            self.circle.setFill(self.color)

            self.text = Text(point, self.text.getText())

            self.print(window)

    def show_arrow_list(self):
        for key in self.arrowList:
            print(self.arrowList[key])

    def print(self, window):

        self.circle.draw(window)
        self.text.draw(window)

        #actualizarea interna
        if self.circle.getCenter() != Point(0, 0):
            for key in self.arrowList:
                self.arrowList[key][1].rewrite(self, self.arrowList[key][0], window)
        self.isPrinted = True

    def unprint(self):
        self.circle.undraw()
        self.text.undraw()

        for key in self.arrowList:
            self.arrowList[key][1].unprint()

        self.isPrinted = False

    def get_center(self):
        return self.circle.getCenter()

    def get_text(self):
        return self.text.getText()

    def get_internal_table(self):
        table = []
        for key in self.arrowList:
            table.append((self.arrowList[key][0].get_text(), self.arrowList[key][1].get_text()))
        return table

    def get_external_table(self, nodeName):
        if self.arrowList.get(nodeName) is not None:
            return self.arrowList[nodeName][0].get_text(), self.arrowList[nodeName][1].get_text()
        else:
            return None

    def verify_state(self, value):
        return stateList[value] in self.state

    def set_state(self, string):
        self.state.append(stateList[string])

    def set_color(self, value):
        self.color = value

    def set_arrow(self, node, arrowValue):
        arrow = Arrow(arrowValue)
        self.arrowList[node.get_text()] = (node, arrow)

    def set_circle(self, point):
        self.circle = Circle(point, self.circle.getRadius())

    def get_next_node_name(self, arrowValue):

        for key in self.arrowList:
            if self.arrowList[key][1].get_text() == arrowValue:
                return self.arrowList[key][0].get_text()

        return None


class Arrow:

    def __init__(self, text):

        self.start, self.finish, self.angle = None, None, None
        self.line = None

        self.center = None
        self.text = Text(Point(0, 0), text)

        self.isPrinted = False

    def __repr__(self):
        return "Arrow {}".format(self.start, self.finish)

    def rewrite(self, start, finish, window):

        if self.isPrinted == True:
            self.unprint()

        if self.isPrinted == False:
            self.start, self.finish, self.angle = self.get_end_points(start, finish)

            self.line = Line(self.start, self.finish)
            self.line.setArrow("last")

            self.center = self.line.getCenter()
            text_pos = Point(self.center.getX() - cos(self.angle + pi / 2) * 20,
                             self.center.getY() - sin(self.angle + pi / 2) * 20)
            self.text = Text(text_pos, self.text.getText())

            self.set_color_properties(white)

            self.print(window)

    def set_color_properties(self, value):
        self.line.setFill(value)
        self.text.setTextColor(value)

    def set_text_properties(self, value):
        self.text.setText(value)

    def print(self, window):
        self.line.draw(window)
        self.text.draw(window)
        self.isPrinted = True

    def unprint(self):
        self.line.undraw()
        self.text.undraw()
        self.isPrinted = False

    def get_text(self):
        return self.text.getText()

    def get_end_points(self, start, finish):
        center1 = start.circle.getCenter()
        c1x = center1.getX()
        c1y = center1.getY()
        r1 = start.circle.getRadius()

        center2 = finish.circle.getCenter()
        c2x = center2.getX()
        c2y = center2.getY()
        r2 = finish.circle.getRadius()

        if c1x != c2x:

            a = atan((c1y - c2y) / (c1x - c2x))  # unghiul liniei fata de ox

            if c1x > c2x:
                startPoint = Point(c1x - r1 * cos(a), c1y - r1 * sin(a))
                finishPoint = Point(c2x + r2 * cos(a), c2y + r2 * sin(a))
            else:

                startPoint = Point(c1x + r1 * cos(a), c1y + r1 * sin(a))
                finishPoint = Point(c2x - r2 * cos(a), c2y - r2 * sin(a))
        else:
            a = pi / 2
            ct = 1.5

            if c1y < c2y:
                startPoint = Point(c1x + ct * r1, c1y + ct * r1)
                finishPoint = Point(c2x + r2, c2y + r2)
            else:
                startPoint = Point(c1x - ct * r1, c1y - ct * r1)
                finishPoint = Point(c2x - r2, c2y - r2)

        return startPoint, finishPoint, a


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


class Graph:
    def __init__(self):
        self.graph = {}
        self.start = None

    def set_graph(self, graph, start):

        for key in graph:
            self.graph[key] = graph[key]

        self.start = start

    def show_nodes(self):
        for key in self.graph:
            print(key)

    def add_node(self, name):
        if self.graph.get(name) is None:
            radius = randint(30, 50)
            self.graph[name] = Node(name, radius)

    def data_to_structure(self, filename):

        with open(filename) as f:

            # prelucrarea nodurilor
            while True:
                line = f.readline().split()

                if line == []:
                    break
                elif line[0] == "start":

                    # adaugarea startului
                    self.add_node(line[1])
                    self.graph[line[1]].set_state("start")
                    self.start = self.graph[line[1]]

                elif line[0] == "end":

                    # adaugarea starilor finale
                    for i in range(1, len(line)):
                        self.add_node(line[i])
                        self.graph[line[i]].set_state("end")

                else:
                    startName, endName, arrowValue = line[0], line[1], line[2]
                    #print(startName, endName, arrowValue)

                    self.add_node(startName)
                    self.add_node(endName)
                    self.graph[startName].set_arrow(self.graph[endName], arrowValue)
        #print(self.graph)

    def verify_word(self, word):

        nextElem = self.start
        if word is None:
            if nextElem.verify_state("end"):
                return "Cuvantul este accept de automat. Procesul s-a terminat cu succes."
            else:
                return "Cuvantul nu este acceptat de automat. Executia s-a oprit la caracterul: {0}.".format(self.start.get_text())

        name = None
        for pair in enumerate(word):
            index, letter = pair

            name = nextElem.get_next_node_name(letter)

            if name is None:
                return "Cuvantul nu e acceptat de automat. Caracterul {0} nu exista.".format(letter)
            else:
                nextElem = self.graph[name]

        if self.graph[name].verify_state("end"):
            return "Cuvantul este acceptat de automat. Procesul s-a terminat cu succes."
        else:
            return "Cuvantul nu este acceptat de automat. Executia s-a oprit la caracterul: {0}."\
                .format(nextElem.get_text())

    def undraw_graph(self, window):

        window.unprint_message()
        for key in self.graph:
            self.graph[key].unprint()

    def draw_graph(self, window):

        for key in self.graph:

            window.print_message("Click pentru a afisa nodul " + key)
            point = window.mouse_click()

            elem = self.graph[key]

            if elem.verify_state("end"):
                #print("primul if")
                self.graph[key].set_color(green)
            elif elem.verify_state("start"):
                #print("al doilea if")
                self.graph[key].set_color(yellow)
            else:
                #print("al treilea if")
                self.graph[key].set_color(red)

            self.graph[key].rewrite(point, window.win)

            for newKey in self.graph:
                self.graph[newKey].rewrite(self.graph[newKey].get_center(), window.win)

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

