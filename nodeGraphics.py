from CONSTANTS_AND_LIBRARIES import *

class Node:

    def __init__(self, text, radius, point=Point(0, 0)):

        self.state = []

        self.circle = Circle(point, radius)

        self.text = Text(point, text)

        self.color = None

        self.arrowList = {}

        self.isPrinted = False

    def update(self, window):
        if self.isPrinted is True:
            for key in self.arrowList:
                if self.arrowList[key][0].isPrinted is True:
                    self.arrowList[key][1].rewrite(self, self.arrowList[key][0], window)

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
            #print(self.circle.getCenter(), Point(0, 0))
            for key in self.arrowList:
                if self.arrowList[key][0].isPrinted is True:
                    self.arrowList[key][1].rewrite(self, self.arrowList[key][0], window)
        self.isPrinted = True

    def unprint(self):
        self.circle.undraw()
        self.text.undraw()

        for key in self.arrowList:
            if self.arrowList[key][1].isPrinted is True:
                self.arrowList[key][1].unprint()

        self.isPrinted = False

    def get_center(self):
        return self.circle.getCenter()

    def get_text(self):
        return self.text.getText()

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