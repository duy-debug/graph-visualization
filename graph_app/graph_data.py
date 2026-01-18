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
    def ensure_node(self, node: str) -> None: # Đảm bảo đỉnh tồn tại trong danh sách nodes và adjacency
        # Kiểm tra xem đỉnh đã có trong danh sách nodes chưa
        if node not in self.nodes:
            # Nếu chưa có, thêm đỉnh vào danh sách nodes
            self.nodes.append(node)
        
        # Kiểm tra xem đỉnh đã có trong dictionary adjacency chưa
        if node not in self.adjacency:
            # Nếu chưa có, tạo một dictionary rỗng cho đỉnh này
            # Dictionary này sẽ lưu các đỉnh kề và trọng số: {đỉnh_kề: trọng_số}
            self.adjacency[node] = {}
    def add_node(self, node: str) -> None: # Thêm một đỉnh mới vào đồ thị
        self.ensure_node(node)
    def remove_node(self, node: str) -> None: # Xóa một đỉnh và các cạnh liên quan khỏi đồ thị
        # Kiểm tra xem đỉnh có tồn tại không
        if node not in self.nodes:
            return  # Nếu không tồn tại, thoát khỏi hàm
        
        # Bước 1: Xóa đỉnh khỏi danh sách nodes
        self.nodes.remove(node)
        
        # Bước 2: Xóa toàn bộ dictionary của đỉnh này trong adjacency
        # pop(node, None) sẽ xóa và trả về giá trị, None là giá trị mặc định nếu không tìm thấy
        self.adjacency.pop(node, None)
        
        # Bước 3: Xóa các cạnh trỏ TỚI đỉnh này từ các đỉnh khác
        # Duyệt qua tất cả các dictionary láng giềng của các đỉnh còn lại
        for nbrs in self.adjacency.values():
            # nbrs là dictionary chứa {đỉnh_kề: trọng_số}
            # Xóa node khỏi dictionary này (nếu có)
            nbrs.pop(node, None)
    def add_edge(self, u: str, v: str, weight: float = 1.0) -> None: # Thêm hoặc cập nhật một cạnh giữa hai đỉnh u và v
        # Bước 1: Đảm bảo cả hai đỉnh u và v đều tồn tại trong đồ thị
        self.ensure_node(u)  # Đảm bảo đỉnh nguồn u tồn tại
        self.ensure_node(v)  # Đảm bảo đỉnh đích v tồn tại
        
        # Bước 2: Xác định trọng số của cạnh
        # Nếu đồ thị có trọng số: sử dụng weight được truyền vào
        # Nếu đồ thị không có trọng số: luôn dùng 1.0
        w = float(weight) if self.weighted else 1.0
        
        # Bước 3: Thêm cạnh u → v với trọng số w
        self.adjacency[u][v] = w
        
        # Bước 4: Nếu là đồ thị vô hướng, thêm cạnh ngược lại v → u
        # Đồ thị vô hướng: cạnh A-B có nghĩa là cả A→B và B→A
        if not self.directed:
            self.adjacency[v][u] = w
    def remove_edge(self, u: str, v: str) -> None: # Xóa cạnh giữa hai đỉnh u và v
        # Bước 1: Xóa cạnh u → v
        # get(u, {}) lấy dictionary láng giềng của u, nếu không có trả về {}
        # pop(v, None) xóa v khỏi dictionary, nếu không có trả về None
        self.adjacency.get(u, {}).pop(v, None)
        
        # Bước 2: Nếu là đồ thị vô hướng, xóa cạnh ngược lại v → u
        if not self.directed:
            self.adjacency.get(v, {}).pop(u, None)
    def load_from_edges( # Nạp dữ liệu đồ thị từ danh sách đỉnh và danh sách cạnh
        self,
        nodes: Iterable[str],
        edges: Iterable[Tuple[str, str, Optional[float]]],
    ) -> None:
        """Nạp dữ liệu đồ thị từ danh sách đỉnh và danh sách cạnh."""
        # Bước 1: Xóa toàn bộ dữ liệu cũ (reset đồ thị)
        self.nodes = []        # Danh sách đỉnh rỗng
        self.adjacency = {}    # Dictionary adjacency rỗng
        
        # Bước 2: Thêm tất cả các đỉnh vào đồ thị
        for node in nodes:
            # node: tên của mỗi đỉnh trong danh sách nodes
            # Chuyển thành string và đảm bảo đỉnh tồn tại
            self.ensure_node(str(node))
        
        # Bước 3: Thêm tất cả các cạnh vào đồ thị
        for edge in edges:
            # edge: một tuple có dạng (u, v) hoặc (u, v, weight)
            # u: đỉnh nguồn, v: đỉnh đích, *rest: các phần tử còn lại (có thể là trọng số)
            u, v, *rest = edge
            
            # Lấy trọng số: nếu có rest[0] thì dùng, không thì dùng 1.0
            weight = rest[0] if rest else 1.0
            
            # Thêm cạnh u → v với trọng số (nếu weight là None thì dùng 1.0)
            self.add_edge(str(u), str(v), weight if weight is not None else 1.0)
    # ------------------------------------------------------------------
    # Biểu diễn dữ liệu
    # ------------------------------------------------------------------
    def adjacency_matrix(self) -> List[List[float]]: # Trả về ma trận kề dưới dạng mảng 2 chiều
        # Khởi tạo ma trận rỗng (danh sách các hàng)
        matrix = []
        
        # Vòng lặp ngoài: Duyệt qua từng đỉnh u (tạo từng hàng của ma trận)
        for u in self.nodes:
            # Khởi tạo hàng rỗng cho đỉnh u
            row = []
            
            # Vòng lặp trong: Duyệt qua từng đỉnh v (tạo từng cột của ma trận)
            for v in self.nodes:
                # Lấy trọng số của cạnh u → v
                # adjacency.get(u, {}) lấy dictionary láng giềng của u, nếu không có trả về {}
                # .get(v, 0.0) lấy trọng số tới v, nếu không có cạnh trả về 0.0
                row.append(self.adjacency.get(u, {}).get(v, 0.0))
            
            # Thêm hàng vừa tạo vào ma trận
            matrix.append(row)
        
        # Trả về ma trận hoàn chỉnh
        # Kết quả: ma trận V x V, với matrix[i][j] = trọng số cạnh nodes[i] → nodes[j]
        return matrix
    def adjacency_list(self) -> Dict[str, List[str]]: # Trả về danh sách kề dưới dạng dictionary (đỉnh -> danh sách các đỉnh kề)
        # Khởi tạo dictionary rỗng để lưu kết quả
        adj_list: Dict[str, List[str]] = {}
        
        # Duyệt qua từng đỉnh trong đồ thị
        for node in self.nodes:
            # Lấy dictionary các đỉnh kề của node hiện tại
            # neighbors có dạng: {đỉnh_kề: trọng_số}
            neighbors = self.adjacency.get(node, {})
            
            # Nếu đồ thị CÓ TRỌNG SỐ: hiển thị dạng "đỉnh (trọng_số)"
            if self.weighted:
                # Khởi tạo danh sách rỗng để lưu các đỉnh kề đã được format
                formatted_neighbors = []
                
                # Duyệt qua từng cặp (đỉnh_kề, trọng_số)
                for nbr, weight in neighbors.items():
                    # nbr: tên đỉnh kề
                    # weight: trọng số của cạnh node → nbr
                    
                    # Trường hợp 1: Trọng số là vô cùng (∞)
                    if weight == float('inf'):
                        formatted_neighbors.append(f"{nbr} (∞)")
                    # Trường hợp 2: Trọng số là số nguyên (ví dụ: 5.0 == 5)
                    elif weight == int(weight):
                        formatted_neighbors.append(f"{nbr} ({int(weight)})")
                    # Trường hợp 3: Trọng số là số thập phân (ví dụ: 3.14)
                    else:
                        # :g là format để loại bỏ các số 0 thừa ở cuối
                        formatted_neighbors.append(f"{nbr} ({weight:g})")
                
                # Lưu danh sách đã format vào kết quả
                adj_list[node] = formatted_neighbors
            
            # Nếu đồ thị KHÔNG TRỌNG SỐ: chỉ hiển thị tên đỉnh
            else:
                # Lấy danh sách các key (tên đỉnh kề) từ dictionary neighbors
                # neighbors.keys() trả về dict_keys(['B', 'C', ...])
                # list(...) chuyển thành ['B', 'C', ...]
                adj_list[node] = list(neighbors.keys())
        
        # Trả về dictionary hoàn chỉnh
        # Kết quả: {đỉnh: [danh_sách_đỉnh_kề]}
        return adj_list
    # ------------------------------------------------------------------
    # Các hàm phân tích bổ sung
    # ------------------------------------------------------------------
    def edge_count(self) -> int: # Đếm tổng số lượng cạnh trong đồ thị
        # Đếm tổng số cạnh bằng cách cộng số láng giềng của tất cả các đỉnh
        # Ví dụ: adjacency = {"A": {"B": 1, "C": 1}, "B": {"A": 1}}
        # -> len({"B": 1, "C": 1}) + len({"A": 1}) = 2 + 1 = 3
        total = sum(len(nbrs) for nbrs in self.adjacency.values())
        
        # Nếu là đồ thị có hướng: trả về total (mỗi cạnh chỉ đếm 1 lần)
        # Nếu là đồ thị vô hướng: chia 2 (vì mỗi cạnh được đếm 2 lần: A->B và B->A)
        return total if self.directed else total // 2
    def density(self) -> float: # Tính toán mật độ của đồ thị (Density)
        # Lấy số lượng đỉnh
        n = len(self.nodes)
        
        # Nếu chỉ có 0 hoặc 1 đỉnh, mật độ = 0
        if n <= 1:
            return 0.0
        
        # Tính số cạnh tối đa có thể có
        # Đồ thị có hướng: n * (n-1) (mỗi đỉnh có thể nối tới n-1 đỉnh khác)
        max_edges = n * (n - 1)
        
        # Đồ thị vô hướng: n * (n-1) / 2 (cạnh A-B và B-A là một)
        if not self.directed:
            max_edges /= 2
        
        # Mật độ = số_cạnh_hiện_tại / số_cạnh_tối_đa
        # Giá trị từ 0.0 (đồ thị thưa) đến 1.0 (đồ thị đầy đủ)
        return self.edge_count() / max_edges if max_edges else 0.0
    def density_label(self, threshold: float = 0.5) -> str: # Phân loại đồ thị là dày (Dense) hay thưa (Sparse) dựa trên ngưỡng mật độ
        # Tính mật độ của đồ thị
        d = self.density()
        
        # So sánh với ngưỡng (mặc định là 0.5 = 50%)
        # Nếu mật độ >= ngưỡng: đồ thị dày (nhiều cạnh)
        # Nếu mật độ < ngưỡng: đồ thị thưa (ít cạnh)
        return "Đồ thị dày" if d >= threshold else "Đồ thị thưa"
    # ------------------------------------------------------------------
    # Chuyển đổi sang thư viện NetworkX
    # ------------------------------------------------------------------
    def to_networkx(self): # Chuyển đổi dữ liệu hiện tại sang đối tượng NetworkX Graph để vẽ họa đồ thị
        # Import thư viện NetworkX (thư viện chuyên dùng cho đồ thị)
        import networkx as nx
        
        # Chọn loại đồ thị NetworkX phù hợp
        # Nếu directed = True: dùng DiGraph (đồ thị có hướng)
        # Nếu directed = False: dùng Graph (đồ thị vô hướng)
        graph_cls = nx.DiGraph if self.directed else nx.Graph
        
        # Tạo đối tượng đồ thị NetworkX rỗng
        g = graph_cls()
        
        # Thêm tất cả các đỉnh vào đồ thị NetworkX
        # add_nodes_from() là hàm có sẵn của NetworkX, nhận vào một danh sách đỉnh
        g.add_nodes_from(self.nodes)
        
        # Thêm tất cả các cạnh vào đồ thị NetworkX
        # Duyệt qua từng đỉnh u và các láng giềng của nó
        for u, neighbors in self.adjacency.items():
            # u: đỉnh nguồn
            # neighbors: dictionary {đỉnh_đích: trọng_số}
            
            # Duyệt qua từng cặp (đỉnh_đích, trọng_số)
            for v, weight in neighbors.items():
                # Điều kiện để tránh thêm cạnh trùng lặp trong đồ thị vô hướng
                # Nếu directed: thêm tất cả cạnh
                # Nếu vô hướng: chỉ thêm cạnh khi u <= v (để tránh thêm cả A->B và B->A)
                if self.directed or (u <= v):
                    # Nếu đồ thị có trọng số: thêm cạnh với thuộc tính weight
                    if self.weighted:
                        g.add_edge(u, v, weight=weight)
                    # Nếu đồ thị không trọng số: thêm cạnh không có weight
                    else:
                        g.add_edge(u, v)
        
        # Trả về đối tượng NetworkX Graph hoàn chỉnh
        return g



