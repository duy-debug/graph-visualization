from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

from .graph_data import GraphData


def parse_edge_line(line: str, weighted: bool) -> Tuple[str, str, float]:
    parts = line.strip().split()
    if len(parts) < 2:
        raise ValueError("Mỗi cạnh cần tối thiểu 2 đỉnh")
    u, v = parts[:2]
    weight = float(parts[2]) if weighted and len(parts) >= 3 else 1.0
    return u, v, weight


def read_graph_from_text(
    text: str, directed: bool = False, weighted: bool = False
) -> GraphData:
    """Định dạng mới:
    Dòng 1: số đỉnh
    Dòng 2: 1 (có hướng) hoặc 0 (vô hướng)
    Các dòng tiếp: u v [w]
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        raise ValueError("File trống")
    
    if len(lines) < 2:
        raise ValueError("File phải có ít nhất 2 dòng (số đỉnh và cờ có hướng)")
    
    # Đọc số đỉnh (dòng 1)
    try:
        num_vertices = int(lines[0])
    except ValueError:
        raise ValueError(f"Dòng 1 phải là số nguyên (số đỉnh), nhận được: {lines[0]}")
    
    # Đọc cờ có hướng (dòng 2)
    try:
        directed_flag = int(lines[1])
        if directed_flag not in [0, 1]:
            raise ValueError("Dòng 2 phải là 0 (vô hướng) hoặc 1 (có hướng)")
        directed = bool(directed_flag)
    except ValueError as e:
        raise ValueError(f"Dòng 2 phải là 0 hoặc 1, nhận được: {lines[1]}") from e
    
    # Đọc các cạnh và tự động phát hiện có trọng số
    edges = []
    nodes_set = set()
    has_weight = False
    
    for i, line in enumerate(lines[2:], start=3):
        parts = line.strip().split()
        if len(parts) < 2:
            raise ValueError(f"Dòng {i}: cạnh cần tối thiểu 2 đỉnh, nhận được: {line}")
        
        u, v = parts[0], parts[1]
        nodes_set.add(u)
        nodes_set.add(v)
        
        # Kiểm tra trọng số
        if len(parts) >= 3:
            try:
                weight = float(parts[2])
                has_weight = True
            except ValueError:
                raise ValueError(f"Dòng {i}: trọng số không hợp lệ '{parts[2]}'")
        else:
            weight = 0.0  # Mặc định là 0 nếu không có trọng số
        
        edges.append((u, v, weight))
    
    # Tự động phát hiện weighted
    weighted = has_weight
    
    # Tạo danh sách nodes từ các cạnh
    nodes = sorted(nodes_set)
    
    # Tạo đồ thị
    graph = GraphData(directed=directed, weighted=weighted)
    graph.load_from_edges(nodes, edges)
    return graph


def read_graph_from_file(
    path: str | Path, directed: bool = False, weighted: bool = False
) -> GraphData:
    return read_graph_from_text(Path(path).read_text(encoding="utf-8"), directed, weighted)


def export_graph_to_file(graph: GraphData, path: str | Path) -> None:
    """Xuất ra file .txt với thông tin cấu trúc đồ thị"""
    nodes = graph.nodes
    node_count = len(nodes)

    # Danh sách cạnh (tránh trùng nếu đồ thị vô hướng)
    edge_lines: List[str] = []
    for u, nbrs in graph.adjacency.items():
        for v, weight in nbrs.items():
            if graph.directed or u <= v:
                if graph.weighted:
                    edge_lines.append(f"{u} {v} {weight:g}")
                else:
                    edge_lines.append(f"{u} {v}")
    if not edge_lines:
        edge_lines.append("∅")

    # Ma trận kề
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

    # Danh sách kề
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

    lines: List[str] = [
        f"Số lượng đỉnh: {node_count}",
        f"Danh sách đỉnh: {', '.join(nodes) if nodes else '∅'}",
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
    import networkx as nx

    base_graph = nx.karate_club_graph()
    data = GraphData(directed=directed, weighted=False)
    nodes = [str(node) for node in base_graph.nodes()]
    edges: List[Tuple[str, str, float]] = []
    for u, v in base_graph.edges():
        edges.append((str(u), str(v), 1.0))
    data.load_from_edges(nodes, edges)
    return data



