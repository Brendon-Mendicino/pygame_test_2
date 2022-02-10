


class Grap:

    def __init__(self):
        self.n_vertices = 0
        self.n_arches
        self.adjacent_list = [[]]
        self.symbol_table = {}
        self.rev_symbol_table = {}

    def add_verticex(self, vertex):
        self.symbol_table[vertex] = self.n_vertices
        self.rev_symbol_table[self.n_vertices] = vertex
        self.adjacent_list[self.n_vertices] = []
        self.n_vertices += 1

    def add_arch(self, arch):
        self.adjacent_list[self.symbol_table[arhc[0]]].append(self.symbol_table[arch[1]])
        self.adjacent_list[self.symbol_table[arhc[1]]].append(self.symbol_table[arch[0]])
