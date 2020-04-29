class simpleGraph:
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

        # for key in self.graph:
        #     if self.dfs(key, []):
        #         newGraph[key] = self.graph[key]

        for key in self.graph:
             if key in self.visited and newGraph.get(key) is None:
                 newGraph[key] = self.graph[key]

        # refacem framework-ul de apel
        self.graph = newGraph
        self.visited = []

        print(self.graph)

    def compare_nodes(self, obj1, obj2, equivalence):

        if len(obj1) != len(obj2):
            return False

        for elem1 in obj1:

            found = False

            for elem2 in obj2:

                if elem1[1] == elem2[1]:
                    if equivalence[elem1[0]] != equivalence[elem2[0]]:
                        return False

                    found = True
                    break

            if found is False:
                return False

        return True

    def compare_tables(self, antTable, curTable):

        if antTable is None:
            return False

        for key in antTable:
            if antTable[key] != curTable[key]:
                return False
        return True

    def get_table(self, antTable):
        tableEquivalence = {}

        if antTable is None:

            print("da")
            for key in self.graph:

                if key in self.exits:
                    tableEquivalence[key] = 1
                else:
                    tableEquivalence[key] = 0
        else:
            print("nu")
            # initializarea id-urilor
            idVal = 0
            for key in antTable:
                if antTable[key] > idVal:
                    idVal = antTable[key] + 1

            for key1 in antTable:
                for key2 in antTable:
                    if key1 != key2:

                        ok = self.compare_nodes(self.graph[key1], self.graph[key2], antTable)
                        #print(key1, ":", self.graph[key1], key2, ":", self.graph[key2], ok)

                        if ok is False:
                            if tableEquivalence.get(key2) is None:

                                is_single = True
                                for key in antTable:
                                    if key2 != key and antTable[key2] == antTable[key]:
                                        is_single = False
                                        break

                                if key2 == 'f':
                                    print(is_single)

                                if is_single is True:
                                    tableEquivalence[key2] = antTable[key2]
                                elif is_single is False:
                                    tableEquivalence[key2] = idVal
                                    idVal += 1
                        else:
                            tableEquivalence[key1] = antTable[key1]
                            tableEquivalence[key2] = antTable[key1]

        return tableEquivalence

    def minimize(self):

        g.delete_inaccessible_nodes()

        antTable = None
        curTable = g.get_table(antTable)
        print("acestea sunt tablele:", antTable, curTable)

        # aplicam myhill-nerode
        while not self.compare_tables(antTable, curTable):
            antTable = curTable
            curTable = g.get_table(antTable)
            print(antTable, curTable)

        rename = {}

        for key in curTable:
            if rename.get(curTable[key]) is None:
                rename[curTable[key]] = key
        #     else:
        #         print("pentru", key, "este deja valoarea", rename[curTable[key]])
        # print(rename)

        # structura de rename ma ajuta sa rescriu corect graful

        newGraph = {}

        for key in self.graph:

            for i in range(len(self.graph[key])):
                self.graph[key][i] = (rename[curTable[self.graph[key][i][0]]], self.graph[key][i][1])

            if key == rename[curTable[key]]:
                newGraph[key] = self.graph[key]

        self.graph = newGraph

        self.start = rename[curTable[self.start]]

        for i in range(len(self.exits)):
            self.exits[i] = rename[curTable[self.exits[i]]]

        #eliminam duplicatele
        self.exits = list(set(self.exits))

g = simpleGraph()
g.data_to_simple_graph("input.txt")
g.minimize()

# print(g.graph)


# print(g.graph)

# def graph_reading():
#
#     w = WindowObject("window", 1000, 800)
#
#     auto = Graph()
#     auto.data_to_structure("input.txt")
#     auto.draw_graph(w)
#     w.unprint_message()
#
#     while True:
#         word = w.read_word()
#         if word is False:
#             break
#         result = auto.verify_word(word)
#         w.print_message(result)
#
# if __name__ == "__main__":
#     #w = WindowObject("DFA", 1000, 600)
#
#     DFA = Graph()
#     DFA.data_to_structure("input.txt")
#
#     DFAMinimized = Graph()
#     DFA.set_graph(*DFA.minimize())
#
#     print(DFAMinimized.graph)
#
#     #DFA.draw_graph(w)
#     #w.mouse_click()
#     #DFA.undraw_graph(w)
#
#     #print("alas")
#     #DFAMinimized = Graph()
#     #print("alas")
#
#     #obj = DFA.minimize_graph()
#
#     #print(len(obj[0]))
#     # for key in obj[0]:
#     #     print(obj[0][key])
#     # DFAMinimized.set_graph(*obj)
#     # DFAMinimized.show_nodes()
#     # print("alas")
#     # DFAMinimized.draw_graph(w)
#     #w.mouse_click()
