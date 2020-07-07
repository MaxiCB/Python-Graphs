from graph.util import Stack, Queue  # These may come in handy


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):
        self.vertices: dict = {}

    def add_vertex(self, vertex_id: int) -> bool:
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()
        return True

    def add_edge(self, v1, v2) -> bool:
        """
        Add a directed edge to the graph.
        """
        if self.vertices[v1] is None or self.vertices[v2] is None:
            raise Exception('One of the provided vertex do not exist')
        self.vertices[v1].add(v2)
        return True

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if self.vertices[vertex_id] is None:
            raise Exception('Invalid vertex')
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        out = []
        out.append(starting_vertex)
        print(starting_vertex)
        q.enqueue(starting_vertex)

        while len(q.queue) > 0:
            u = q.queue[0]
            curr = self.vertices[u]
            for v in curr:
                if v not in out:
                    out.append(v)
                    print(v)
                    q.enqueue(v)
            q.dequeue()

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        visited = []
        s = Stack()
        s.push(starting_vertex)
        while s.size() > 0:
            v = s.pop()
            if v not in visited:
                print(v)
                visited.append(v)
                for i in self.get_neighbors(v):
                    s.push(i)

    def dft_recursive(self, starting_vertex, visited=[]):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        visited.append(starting_vertex)
        if len(visited) == 1:
            print(starting_vertex)
        for i in self.get_neighbors(starting_vertex):
            if i not in visited:
                visited.append(i)
                print(i)
                self.dft_recursive(i)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        visited = set()
        q = Queue()
        q.enqueue([1])
        paths = {}
        while (q.size() > 0):
            path = q.dequeue()
            v = path[-1]
            if (v == destination_vertex):
                length = len(path)
                if (length in paths):
                    paths[length].append(path)
                else:
                    paths[length] = [path]
            elif (not v in visited):
                visited.add(v)
                for neighbor in self.vertices[v]:
                    q.enqueue([*path, neighbor])
        smallest = min(paths.keys())
        return None if len(paths[smallest]) == 0 else paths[smallest] if len(paths[smallest]) > 1 else paths[smallest][
            0]

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        visited = set()
        s = Stack()
        s.push([1])
        paths = {}
        while (s.size() > 0):
            path = s.pop()
            v = path[-1]
            if (v == destination_vertex):
                length = len(path)
                if (length in paths):
                    paths[length].append(path)
                else:
                    paths[length] = [path]
            elif (v not in visited):
                visited.add(v)
                for neighbor in self.vertices[v]:
                    s.push([*path, neighbor])
        smallest = min(paths.keys())
        return None if len(paths[smallest]) == 0 else paths[smallest] if len(paths[smallest]) > 1 else paths[smallest][
            0]

    def dfs_recursive(self, starting_vertex, destination_vertex, visited_set=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        This should be done using recursion.
        """
        if visited_set is None:
            visited_set = set()

        if path is None:
            path = []

        visited_set.add(starting_vertex)

        # set the path to be the initial path and at the starting_vertex
        path = path + [starting_vertex]

        # if we've found the target vertex return the path
        if starting_vertex == destination_vertex:
            return path

        # loop over the connected vertices
        for vertex in self.vertices[starting_vertex]:
            # if visited, do nothing
            # if not visited recurse
            if vertex not in visited_set:
                # recurse setting path by passing in the vertex, destination vertex the visited_set, path and store
                new_path = self.dfs_recursive(vertex, destination_vertex, visited_set, path)

                # if the new path is None return new path
                if new_path is not None:
                    return new_path
        return None


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))