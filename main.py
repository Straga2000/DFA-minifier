from automata import *
from windowGraphics import *

if __name__ == "__main__":

    filename = "input1.txt"

    w = WindowObject("DFA", 1000, 600)
    w.disable_reader()

    normalGraph = Graph()
    normalGraph.data_to_structure(filename)
    normalGraph.draw_graph(w)
    w.mouse_click()

    normalGraph.undraw_graph(w)

    minimizedGraph = SimpleGraph()
    minimizedGraph.data_to_simple_graph(filename)
    minimizedGraph.minimize()

    normalGraph.set_graph(minimizedGraph.get_structure())
    normalGraph.draw_graph(w)
    w.mouse_click()


