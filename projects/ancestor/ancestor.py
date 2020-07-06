from util import Queue, Stack

class Graph():
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edges(self, v1, v2):
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError('That vertex does not exist')

def earliest_ancestor(ancestors, starting_node):
    s = Stack()
    s.push(starting_node)
    visited = set()
    first_ancestor = -1

    while s.size() > 0:
        v = s.pop()
        if v not in visited:
            visited.add(v)
            
            for ancestor in ancestors:
                if ancestor[1] == v:
                    s.push(ancestor[0])
                    if first_ancestor == -1:
                        first_ancestor = ancestor[0]
                    
                    parents = []

                    for a in ancestors:
                        if a[1] == v:
                            parents.append(a[0])

                            if len(parents) == 1:
                                first_ancestor = a[0]
                            else:
                                if first_ancestor > a[0]:
                                    first_ancestor = a[0]
        
    return first_ancestor

if __name__ == '__main__':
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    earliest_ancestor(test_ancestors, 1)
