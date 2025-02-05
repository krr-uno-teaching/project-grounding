from dataclasses import dataclass, field
from typing import Dict, Generic, List, Tuple, TypeVar

T = TypeVar("T")  # pylint: disable=invalid-name
U = TypeVar("U", int, Tuple[int, int])  # pylint: disable=invalid-name


@dataclass
class Vertex(Generic[T]):
    """
    Vertex data to calculate SCCs of a graph.
    """

    name: T
    visited: int
    index: int = 0
    edges: List[int] = field(default_factory=list)


class Graph(Generic[T]):
    """
    Simple class to compute strongly connected components using Tarjan's
    algorithm.
    """

    _names: Dict[T, int]
    _vertices: List[Vertex]
    _phase: bool

    def __init__(self):
        self._names = {}
        self._vertices = []
        self._phase = True

    def _visited(self, key_u: int) -> bool:
        return self._vertices[key_u].visited != int(not self._phase)

    def _active(self, key_u: int) -> bool:
        return self._vertices[key_u].visited != int(self._phase)

    def _addvertex(self, val_u: T) -> int:
        n = len(self._vertices)
        key_u = self._names.setdefault(val_u, n)
        if n == key_u:
            self._vertices.append(Vertex(val_u, int(not self._phase)))
        return key_u

    def add_edge(self, val_u: T, val_v: T) -> None:
        """
        Add an edge to the graph.
        """
        key_u = self._addvertex(val_u)
        key_v = self._addvertex(val_v)
        self._vertices[key_u].edges.append(key_v)

    def tarjan(self) -> List[List[T]]:
        """
        Returns the strictly connected components of the graph.
        """
        sccs: List[List[T]] = []
        stack = []
        trail = []
        index = 1

        def push(key_u: int):
            nonlocal index
            index += 1
            vtx_u = self._vertices[key_u]
            vtx_u.visited = index
            vtx_u.index = 0
            stack.append(key_u)
            trail.append(key_u)

        for key_u in range(len(self._vertices)):
            if self._visited(key_u):
                continue
            index = 1
            push(key_u)
            while stack:
                key_v = stack[-1]
                vtx_v = self._vertices[key_v]
                len_v = len(vtx_v.edges)
                while vtx_v.index < len_v:
                    key_w = vtx_v.edges[vtx_v.index]
                    vtx_v.index += 1
                    if not self._visited(key_w):
                        push(key_w)
                        break
                else:
                    stack.pop()
                    root = True
                    for key_w in vtx_v.edges:
                        vtx_w = self._vertices[key_w]
                        if self._active(key_w) and vtx_w.visited < vtx_v.visited:
                            root = False
                            vtx_v.visited = vtx_w.visited
                    if root:
                        key_last = None
                        sccs.append([])
                        while key_last != key_v:
                            key_last = trail[-1]
                            vtx_last = self._vertices[key_last]
                            sccs[-1].append(vtx_last.name)
                            vtx_last.visited = int(self._phase)
                            trail.pop()
                        # if len(sccs[-1]) == 1:
                        #     sccs.pop()

        self._phase = not self._phase
        return sccs

    def sccs(self) -> list[list[T]]:
        """
        Returns the strongly connected components of the graph in topological order.
        """
        sccs = self.tarjan()
        sccs.reverse()
        return sccs

    def __str__(self) -> str:
        edges = []
        for origin in self._vertices:
            for dest_int in origin.edges:
                destination = self._vertices[dest_int]
                origin_str = f'"{str(origin.name)}"'
                destination_str = f'"{str(destination.name)}"'
                edges.append(f"{origin_str:40} \t==>\t {destination_str}")
        return "\n".join(edges)
