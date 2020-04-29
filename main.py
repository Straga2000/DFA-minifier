from automata import *
from windowGraphics import *

if __name__ == "__main__":
    w = WindowObject("DFA", 1000, 600)

    normalGraph = Graph()
    normalGraph.data_to_structure("input.txt")
    normalGraph.draw_graph(w)
    w.mouse_click()

    normalGraph.undraw_graph(w)

    minimizedGraph = SimpleGraph()
    minimizedGraph.data_to_simple_graph("input.txt")
    minimizedGraph.minimize()

    normalGraph.set_graph(minimizedGraph.get_structure())
    normalGraph.draw_graph(w)
    w.mouse_click()


