from __future__ import annotations
from pathlib import Path
from typing import List, Tuple
from .graph_data import GraphData

def read_graph_from_text(
    text: str, directed: bool = False, weighted: bool = False
) -> GraphData:
    """
    Đọc dữ liệu đồ thị từ một chuỗi văn bản.
    Định dạng quy định:
    - Dòng 1: Số lượng đỉnh (Số nguyên).
    - Dòng 2: Cờ đồ thị có hướng (1) hoặc vô hướng (0).
    - Các dòng tiếp theo: Danh sách cạnh theo định dạng 'u v [w]' (u: nguồn, v: đích, w: trọng số tùy chọn).
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Nội dung dữ liệu trống.")
    if len(lines) < 2:
        raise ValueError("Dữ liệu phải có ít nhất 2 dòng: dòng 1 là số đỉnh, dòng 2 là cờ có hướng (0/1).")

    # 1. Đọc số lượng đỉnh (Dòng 1)
    try:
        num_vertices = int(lines[0])
    except ValueError:
        raise ValueError(f"Lỗi dòng 1: Phải là số nguyên (số lượng đỉnh). Nhận được: '{lines[0]}'")

    # 2. Đọc cờ có hướng (Dòng 2)
    try:
        directed_flag = int(lines[1])
        if directed_flag not in [0, 1]:
            raise ValueError("Cờ có hướng phải là 0 hoặc 1.")
        directed = bool(directed_flag)
    except ValueError as e:
        raise ValueError(f"Lỗi dòng 2: Phải là 0 hoặc 1. Nhận được: '{lines[1]}'") from e

    # 3. Đọc danh sách các cạnh
    edges = []
    nodes_set = set()
    has_weight = False
    for i, line in enumerate(lines[2:], start=3):
        parts = line.strip().split()
        if len(parts) < 2:
            # Nếu dòng chỉ có 1 phần tử, coi đó là đỉnh đơn lẻ
            nodes_set.add(parts[0])
            continue
        u, v = parts[0], parts[1]
        nodes_set.add(u)
        nodes_set.add(v)  
        # Kiểm tra sự tồn tại của trọng số
        if len(parts) >= 3:
            try:
                weight = float(parts[2])
                has_weight = True
            except ValueError:
                raise ValueError(f"Lỗi dòng {i}: Trọng số '{parts[2]}' không hợp lệ (phải là số).")
        else:
            weight = 0.0  # Gán mặc định là 0 nếu không nhập trọng số
        
        edges.append((u, v, weight))

    # Tự động gán trạng thái Weighted nếu có ít nhất một cạnh có trọng số
    weighted = has_weight
    
    # Tạo danh sách các đỉnh theo thứ tự nhất quán
    nodes = sorted(nodes_set)
    
    # Khởi tạo đối tượng GraphData và nạp dữ liệu
    graph = GraphData(directed=directed, weighted=weighted)
    graph.load_from_edges(nodes, edges)
    return graph

def read_graph_from_file(
    path: str | Path, directed: bool = False, weighted: bool = False
) -> GraphData:
    """Đọc dữ liệu đồ thị từ tệp tin cục bộ."""
    return read_graph_from_text(Path(path).read_text(encoding="utf-8"), directed, weighted)

def export_graph_to_file(graph: GraphData, path: str | Path) -> None:
    """
    Xuất cấu trúc đồ thị hiện tại ra tệp tin văn bản (.txt) kèm theo báo cáo chi tiết.
    Bao gồm: thuộc tính đồ thị, ma trận kề, danh sách kề và danh sách cạnh.
    """
    nodes = graph.nodes
    node_count = len(nodes)

    # 1. Tạo danh sách cạnh (Lọc trùng lặp nếu đồ thị vô hướng)
    edge_lines: List[str] = []
    for u, nbrs in graph.adjacency.items():
        for v, weight in nbrs.items():
            if graph.directed or u <= v:
                if graph.weighted:
                    edge_lines.append(f"{u} {v} {weight:g}")
                else:
                    edge_lines.append(f"{u} {v}")
    if not edge_lines:
        edge_lines.append("∅ (Đồ thị rỗng)")

    # 2. Xây dựng ma trận kề dạng bảng
    matrix = graph.adjacency_matrix()
    matrix_lines: List[str] = []
    if nodes:
        header = ["#"] + nodes
        matrix_lines.append("\t".join(header))
        for idx, row in enumerate(matrix):
            u = nodes[idx]
            row_values: List[str] = [nodes[idx]]
            for col_idx, val in enumerate(row):
                v = nodes[col_idx]
                weight = graph.adjacency.get(u, {}).get(v)
                if graph.weighted:
                    row_values.append("INF" if weight is None else f"{weight:g}")
                else:
                    row_values.append(f"{val:g}")
            matrix_lines.append("\t".join(row_values))
    else:
        matrix_lines.append("∅")

    # 3. Xây dựng danh sách kề
    adjacency_list = graph.adjacency_list()
    adj_list_lines: List[str] = []
    if nodes:
        for node in nodes:
            neighbors = adjacency_list.get(node, [])
            adj_list_lines.append(
                f"{node} -> {', '.join(neighbors) if neighbors else '∅'}"
            )
    else:
        adj_list_lines.append("∅")

    # Tổng hợp nội dung file xuất
    lines: List[str] = [
        f"Số lượng đỉnh: {node_count}",
        f"Đồ thị: {'có hướng' if graph.directed else 'vô hướng'}",
        f"Trọng số: {'có' if graph.weighted else 'không'}",
        "",
        "Danh sách cạnh:",
        *edge_lines,
        "",
        "Ma trận kề:",
        *matrix_lines,
        "",
        "Danh sách kề:",
        *adj_list_lines,
    ]
    Path(path).write_text("\n".join(lines), encoding="utf-8")

def load_karate_club(directed: bool = False) -> GraphData:
    """Tải đồ thị mẫu nổi tiếng - Zachary's Karate Club từ thư viện NetworkX."""
    import networkx as nx
    base_graph = nx.karate_club_graph()
    data = GraphData(directed=directed, weighted=False)
    nodes = [str(node) for node in base_graph.nodes()]
    edges: List[Tuple[str, str, float]] = []
    for u, v in base_graph.edges():
        edges.append((str(u), str(v), 1.0))
    data.load_from_edges(nodes, edges)
    return data



