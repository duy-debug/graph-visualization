from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Iterable, Optional

@dataclass
class GraphData:
    """
    Lớp quản lý dữ liệu đồ thị (Model).
    Lưu trữ cấu trúc đỉnh, cạnh và trọng số, cung cấp các phép toán cơ bản trên đồ thị.
    """
    directed: bool = False  # Đồ thị có hướng hay không
    weighted: bool = False  # Đồ thị có trọng số hay không
    nodes: List[str] = field(default_factory=list)  # Danh sách các đỉnh
    adjacency: Dict[str, Dict[str, float]] = field(default_factory=dict)  # Biểu diễn ma trận kề bằng dictionary

    # ------------------------------------------------------------------
    # Cập nhật dữ liệu
    # ------------------------------------------------------------------
    
    def ensure_node(self, node: str) -> None:
        """Đảm bảo đỉnh tồn tại trong danh sách nodes và adjacency."""
        if node not in self.nodes:
            self.nodes.append(node)
        if node not in self.adjacency:
            self.adjacency[node] = {}

    def add_node(self, node: str) -> None:
        """Thêm một đỉnh mới vào đồ thị."""
        self.ensure_node(node)

    def remove_node(self, node: str) -> None:
        """Xóa một đỉnh và các cạnh liên quan khỏi đồ thị."""
        if node not in self.nodes:
            return
        self.nodes.remove(node)
        self.adjacency.pop(node, None)
        # Xóa các cạnh trỏ tới đỉnh này trong các danh sách kề khác
        for nbrs in self.adjacency.values():
            nbrs.pop(node, None)

    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None:
        """Thêm hoặc cập nhật một cạnh giữa hai đỉnh u và v."""
        self.ensure_node(u)
        self.ensure_node(v)
        w = float(weight) if self.weighted else 1.0
        self.adjacency[u][v] = w
        # Nếu là đồ thị vô hướng, thêm cạnh ngược lại
        if not self.directed:
            self.adjacency[v][u] = w

    def remove_edge(self, u: str, v: str) -> None:
        """Xóa cạnh giữa hai đỉnh u và v."""
        self.adjacency.get(u, {}).pop(v, None)
        if not self.directed:
            self.adjacency.get(v, {}).pop(u, None)

    def load_from_edges(
        self,
        nodes: Iterable[str],
        edges: Iterable[Tuple[str, str, Optional[float]]],
    ) -> None:
        """Nạp dữ liệu đồ thị từ danh sách đỉnh và danh sách cạnh."""
        self.nodes = []
        self.adjacency = {}
        for node in nodes:
            self.ensure_node(str(node))
        for edge in edges:
            u, v, *rest = edge
            weight = rest[0] if rest else 1.0
            self.add_edge(str(u), str(v), weight if weight is not None else 1.0)

    # ------------------------------------------------------------------
    # Biểu diễn dữ liệu
    # ------------------------------------------------------------------

    def adjacency_matrix(self) -> List[List[float]]:
        """Trả về ma trận kề dưới dạng mảng 2 chiều."""
        matrix = []
        for u in self.nodes:
            row = []
            for v in self.nodes:
                row.append(self.adjacency.get(u, {}).get(v, 0.0))
            matrix.append(row)
        return matrix

    def adjacency_list(self) -> Dict[str, List[str]]:
        """Trả về danh sách kề dưới dạng dictionary (đỉnh -> danh sách các đỉnh kề)."""
        adj_list: Dict[str, List[str]] = {}
        for node in self.nodes:
            neighbors = self.adjacency.get(node, {})
            if self.weighted:
                # Nếu có trọng số, định dạng: "v (w)"
                formatted_neighbors = []
                for nbr, weight in neighbors.items():
                    if weight == float('inf'):
                        formatted_neighbors.append(f"{nbr} (∞)")
                    elif weight == int(weight):
                        formatted_neighbors.append(f"{nbr} ({int(weight)})")
                    else:
                        formatted_neighbors.append(f"{nbr} ({weight:g})")
                adj_list[node] = formatted_neighbors
            else:
                adj_list[node] = list(neighbors.keys())
        return adj_list

    # ------------------------------------------------------------------
    # Các hàm phân tích bổ sung
    # ------------------------------------------------------------------

    def edge_count(self) -> int:
        """Đếm tổng số lượng cạnh trong đồ thị."""
        total = sum(len(nbrs) for nbrs in self.adjacency.values())
        return total if self.directed else total // 2

    def density(self) -> float:
        """Tính toán mật độ của đồ thị (Density)."""
        n = len(self.nodes)
        if n <= 1:
            return 0.0
        max_edges = n * (n - 1)
        if not self.directed:
            max_edges /= 2
        return self.edge_count() / max_edges if max_edges else 0.0

    def density_label(self, threshold: float = 0.5) -> str:
        """Phân loại đồ thị là dày (Dense) hay thưa (Sparse) dựa trên ngưỡng mật độ."""
        d = self.density()
        return "Đồ thị dày" if d >= threshold else "Đồ thị thưa"

    # ------------------------------------------------------------------
    # Chuyển đổi sang thư viện NetworkX
    # ------------------------------------------------------------------

    def to_networkx(self):
        """Chuyển đổi dữ liệu hiện tại sang đối tượng NetworkX Graph để vẽ họa đồ."""
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



