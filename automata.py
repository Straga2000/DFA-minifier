from nodeGraphics import *

class SimpleGraph:
    def __init__(self):
        self.graph = {}
        self.start = None
        self.exits = []
        self.visited = []

    def data_to_simple_graph(self, filename):
        with open(filename) as f:
            while True:
                line = f.readline().split()

                if line == []:
                    break
                elif line[0] == "start":
                    if self.graph.get(line[1]) is None:
                        self.graph[line[1]] = []
                    self.start = line[1]

                elif line[0] == "end":

                    for i in range(1, len(line)):
                        if self.graph.get(line[i]) is None:
                            self.graph[line[i]] = []
                        self.exits.append(line[i])
                else:

                    if self.graph.get(line[0]) is None:
                        self.graph[line[0]] = []

                    if self.graph.get(line[1]) is None:
                        self.graph[line[1]] = []

                    self.graph[line[0]].append((line[1], line[2]))

    def bfs(self, node):
        for elem in self.graph[node]:
            if elem[0] not in self.visited:
                self.visited.append(elem[0])
                self.bfs(elem[0])

    def dfs(self, node, visited):
        if node in self.exits:
            return True
        else:
            if node not in visited:

                visited.append(node)
                value = False

                for elem in self.graph[node]:
                    value = value or self.dfs(elem[0], visited)

                return value

        return False

    def delete_inaccessible_nodes(self):
        self.visited = []
        self.bfs(self.start)

        newGraph = {}

        for key in self.graph:
             if key in self.visited and newGraph.get(key) is None:
                 newGraph[key] = self.graph[key]

        # refacem framework-ul de apel
        self.graph = newGraph
        self.visited = []

        #print(self.graph)

    def compare_nodes(self, obj1, obj2, equivalence):

        if len(obj1) != len(obj2):
            return False

        for elem1 in obj1:

            found = False

            for elem2 in obj2:
                if elem1[1] == elem2[1]:
                    #print(elem1[0], elem2[0])
                    for line in equivalence:
                        if elem2[0] in line and elem1[0] not in line:
                            return False

                    found = True
                    break

            if found is False:
                return False

        return True

    def get_signature(self, table):
        if table is None:
            return [0]
        return [len(line) for line in table]


    def get_table(self, antTable):

        table = []
        if antTable is None:

            # construim primele doua multimi
            table.append([])
            table.append([])

            for key in self.graph:
                if key in self.exits:
                    table[0].append(key)
                else:
                    table[1].append(key)
        else:

            #initializarea tabelului
            for line in antTable:

                newLine = []
                for i in range(len(line)):
                    newLine.append(line[i])

                table.append(newLine)

            for line in table:

                newLine = []
                for i in range(len(line)):

                    verify = True
                    for j in range(i):
                        if line[i] != 0 and line[j] != 0:
                            if not self.compare_nodes(self.graph[line[i]], self.graph[line[j]], antTable):
                                verify = False
                                break

                    if verify is False:
                        newLine.append(line[i])
                        line[i] = 0

                if len(newLine) != 0:
                    table.append(newLine)
        return table

    def minimize(self):

        curTable = None
        while True:
            antTable = curTable
            curTable = self.get_table(antTable)

            if self.get_signature(antTable) == self.get_signature(curTable):
                break

        #print(curTable)
        #clean the table
        rename = {}

        for line in curTable:
            for i in range(len(line)):
                if line[i] != 0:
                    rename[line[i]] = line[0]

        #print(rename)

        newGraph = {}

        for key in self.graph:

            if key == rename[key]:

                newGraph[key] = self.graph[key]
                for i in range(len(self.graph[key])):
                    self.graph[key][i] = (rename[self.graph[key][i][0]], self.graph[key][i][1])

        self.graph = newGraph

        self.start = rename[self.start]

        for i in range(len(self.exits)):
             self.exits[i] = rename[self.exits[i]]

        #eliminam duplicatele
        self.exits = list(set(self.exits))

    # def minimize(self):
    #
    #     self.delete_inaccessible_nodes()
    #
    #     antTable = None
    #     curTable = self.get_table(antTable)
    #
    #     # aplicam myhill-nerode
    #     while not self.compare_tables(antTable, curTable):
    #         antTable = curTable
    #         curTable = self.get_table(antTable)
    #         print(antTable, curTable)
    #
    #     rename = {}
    #
    #     for key in curTable:
    #         if rename.get(curTable[key]) is None:
    #             rename[curTable[key]] = key
    #     # structura de rename ma ajuta sa rescriu corect graful
    #
    #     newGraph = {}
    #
    #     for key in self.graph:
    #
    #         for i in range(len(self.graph[key])):
    #             self.graph[key][i] = (rename[curTable[self.graph[key][i][0]]], self.graph[key][i][1])
    #
    #         if key == rename[curTable[key]]:
    #             newGraph[key] = self.graph[key]
    #
    #     self.graph = newGraph
    #
    #     self.start = rename[curTable[self.start]]
    #
    #     for i in range(len(self.exits)):
    #         self.exits[i] = rename[curTable[self.exits[i]]]
    #
    #     #eliminam duplicatele
    #     self.exits = list(set(self.exits))

    def get_structure(self):
        return self.graph, self.start, self.exits

class Graph:
    def __init__(self):
        self.graph = {}
        self.start = None

    def set_graph(self, obj):
        graph, start, exits = obj

        for key in graph:

            if key == start:
                self.add_node_with_state(key, "start")
                self.start = self.graph[key]
            elif key in exits:
                self.add_node_with_state(key, "end")
            else:
                self.add_node(key)

            for elem in graph[key]:
                if elem[0] == start:
                    self.add_node_with_state(elem[0], "start")
                    self.start = self.graph[elem[0]]
                elif key in exits:
                    self.add_node_with_state(elem[0], "end")
                else:
                    self.add_node(elem[0])

                self.graph[key].set_arrow(self.graph[elem[0]], elem[1])

    def show_nodes(self):
        for key in self.graph:
            print(key)

    def add_node(self, name):
        if self.graph.get(name) is None:
            radius = randint(30, 50)
            self.graph[name] = Node(name, radius)

    def add_node_with_state(self, name, state="nothing"):
        if self.graph.get(name) is None:
            radius = randint(30, 50)
            self.graph[name] = Node(name, radius)
        self.graph[name].set_state(state)

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

        self.clean_graph()

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
                self.graph[newKey].update(window.win)

    def clean_graph(self):
        self.graph = {}
        self.start = None