from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Iterable, Optional
@dataclass
class GraphData:
    """Biểu diễn đồ thị linh hoạt cho UI."""
    directed: bool = False
    weighted: bool = False
    nodes: List[str] = field(default_factory=list)
    adjacency: Dict[str, Dict[str, float]] = field(default_factory=dict)
    # ------------------------------------------------------------------
    # Tạo / cập nhật dữ liệu
    # ------------------------------------------------------------------
    def ensure_node(self, node: str) -> None:
        if node not in self.nodes:
            self.nodes.append(node)
        if node not in self.adjacency:
            self.adjacency[node] = {}
    def add_node(self, node: str) -> None:
        self.ensure_node(node)
    def remove_node(self, node: str) -> None:
        if node not in self.nodes:
            return
        self.nodes.remove(node)
        self.adjacency.pop(node, None)
        for nbrs in self.adjacency.values():
            nbrs.pop(node, None)
    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        self.ensure_node(u)
        self.ensure_node(v)
        w = float(weight) if self.weighted else 1.0
        self.adjacency[u][v] = w
        if not self.directed:
            self.adjacency[v][u] = w
    def remove_edge(self, u: str, v: str) -> None:
        self.adjacency.get(u, {}).pop(v, None)
        if not self.directed:
            self.adjacency.get(v, {}).pop(u, None)
    def load_from_edges(
        self,
        nodes: Iterable[str],
        edges: Iterable[Tuple[str, str, Optional[float]]],
    ) -> None:
        self.nodes = []
        self.adjacency = {}
        for node in nodes:
            self.ensure_node(str(node))
        for edge in edges:
            u, v, *rest = edge
            weight = rest[0] if rest else 1.0
            self.add_edge(str(u), str(v), weight if weight is not None else 1.0)
    # ------------------------------------------------------------------
    # Cấu trúc dữ liệu
    # ------------------------------------------------------------------
    def adjacency_matrix(self) -> List[List[float]]:
        matrix = []
        for u in self.nodes:
            row = []
            for v in self.nodes:
                row.append(self.adjacency.get(u, {}).get(v, 0.0))
            matrix.append(row)
        return matrix
    def adjacency_list(self) -> Dict[str, List[str]]:
        adj_list: Dict[str, List[str]] = {}
        for node in self.nodes:
            neighbors = self.adjacency.get(node, {})
            if self.weighted:
                # Hiển thị số nguyên nếu trọng số là số nguyên
                formatted_neighbors = []
                for nbr, weight in neighbors.items():
                    if weight == int(weight):
                        formatted_neighbors.append(f"{nbr} ({int(weight)})")
                    else:
                        formatted_neighbors.append(f"{nbr} ({weight:g})")
                adj_list[node] = formatted_neighbors
            else:
                adj_list[node] = list(neighbors.keys())
        return adj_list
    # ------------------------------------------------------------------
    # Phân tích
    # ------------------------------------------------------------------
    def edge_count(self) -> int:
        total = sum(len(nbrs) for nbrs in self.adjacency.values())
        return total if self.directed else total // 2
    def density(self) -> float:
        n = len(self.nodes)
        if n <= 1:
            return 0.0
        max_edges = n * (n - 1)
        if not self.directed:
            max_edges /= 2
        return self.edge_count() / max_edges if max_edges else 0.0

    def density_label(self, threshold: float = 0.5) -> str:
        d = self.density()
        return "Đồ thị dày" if d >= threshold else "Đồ thị thưa"
    # ------------------------------------------------------------------
    # NetworkX tiện ích
    # ------------------------------------------------------------------
    def to_networkx(self):
        import networkx as nx
        graph_cls = nx.DiGraph if self.directed else nx.Graph
        g = graph_cls()
        g.add_nodes_from(self.nodes)
        for u, neighbors in self.adjacency.items():
            for v, weight in neighbors.items():
                if self.directed or (u <= v):
                    if self.weighted:
                        g.add_edge(u, v, weight=weight)
                    else:
                        g.add_edge(u, v)
        return g



