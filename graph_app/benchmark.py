from __future__ import annotations
import time
import random
import sys
from pathlib import Path
from typing import List, Tuple, Dict
from dataclasses import dataclass
# Import các module của ứng dụng
from .graph_data import GraphData

@dataclass
class BenchmarkResult:
    """Lớp lưu trữ kết quả benchmark cho một cấu hình test."""
    n_nodes: int                    # Số lượng đỉnh
    density: float                  # Mật độ đồ thị (0.0 - 1.0)
    n_edges: int                    # Số cạnh thực tế
    directed: bool                  # Đồ thị có hướng
    weighted: bool                  # Đồ thị có trọng số
    
    # Thời gian xử lý cấu trúc dữ liệu (ms)
    create_structure_time: float    # Thời gian tạo cấu trúc dữ liệu
    check_edge_time: float          # Thời gian kiểm tra cạnh (1000 lần)
    get_neighbors_time: float       # Thời gian lấy danh sách kề (1000 lần)
    create_matrix_time: float       # Thời gian tạo ma trận kề
    create_adj_list_time: float     # Thời gian tạo danh sách kề
    
    # Thời gian vẽ/hiển thị (ms) - nếu có
    draw_time: float = 0.0          # Thời gian vẽ đồ thị (Matplotlib)


def generate_random_graph( # Tạo đồ thị ngẫu nhiên với số đỉnh và mật độ cho trước
    n_nodes: int, 
    density: float, 
    directed: bool = False, 
    weighted: bool = False,
    seed: int = None
) -> Tuple[List[str], List[Tuple[str, str, float]]]:
    """
    Tạo đồ thị ngẫu nhiên với số đỉnh và mật độ cho trước.
    
    Args:
        n_nodes: Số lượng đỉnh
        density: Mật độ đồ thị (0.0 đến 1.0)
        directed: True nếu đồ thị có hướng
        weighted: True nếu đồ thị có trọng số
        seed: Seed cho random (để kết quả có thể lặp lại)
    
    Returns:
        Tuple gồm danh sách đỉnh và danh sách cạnh
    """
    # Thiết lập seed để kết quả có thể lặp lại (reproducible)
    if seed is not None:
        random.seed(seed)
    
    # Bước 1: Tạo danh sách đỉnh từ 0 đến n_nodes-1 (dạng chuỗi)
    # Ví dụ: n_nodes=5 → nodes = ["0", "1", "2", "3", "4"]
    nodes = [str(i) for i in range(n_nodes)]
    
    # Bước 2: Tính số cạnh tối đa có thể có trong đồ thị
    # - Đồ thị có hướng: n*(n-1) (mỗi đỉnh nối với n-1 đỉnh khác, 2 chiều)
    # - Đồ thị vô hướng: n*(n-1)/2 (mỗi cặp đỉnh chỉ có 1 cạnh)
    if directed:
        max_edges = n_nodes * (n_nodes - 1)
    else:
        max_edges = n_nodes * (n_nodes - 1) // 2
    
    # Bước 3: Tính số cạnh mục tiêu dựa trên mật độ
    # Ví dụ: max_edges=100, density=0.3 → target_edges=30
    target_edges = int(max_edges * density)
    
    # Bước 4: Tạo tất cả các cặp đỉnh có thể (không bao gồm cạnh tự nối)
    all_pairs = []
    for i in range(n_nodes):
        for j in range(n_nodes):
            if i != j:  # Không cho phép cạnh tự nối (i→i)
                if directed:
                    # Đồ thị có hướng: thêm cả (i,j) và (j,i)
                    all_pairs.append((str(i), str(j)))
                elif i < j:  # Đồ thị vô hướng: chỉ lấy i<j để tránh trùng lặp
                    all_pairs.append((str(i), str(j)))
    
    # Bước 5: Chọn ngẫu nhiên số cạnh cần thiết từ tất cả các cặp có thể
    # random.sample() đảm bảo không chọn trùng lặp
    selected_pairs = random.sample(all_pairs, min(target_edges, len(all_pairs)))
    
    # Bước 6: Tạo danh sách cạnh với trọng số
    edges = []
    for u, v in selected_pairs:
        if weighted:
            # Đồ thị có trọng số: random từ 1.0 đến 10.0, làm tròn 1 chữ số
            weight = round(random.uniform(1.0, 10.0), 1)
        else:
            # Đồ thị không trọng số: mặc định = 1.0
            weight = 1.0
        edges.append((u, v, weight))
    
    # Trả về tuple (danh sách đỉnh, danh sách cạnh)
    return nodes, edges

def measure_create_structure(nodes: List[str], edges: List[Tuple], directed: bool, weighted: bool) -> Tuple[GraphData, float]: # Đo thời gian tạo cấu trúc dữ liệu đồ thị
    """
    Đo thời gian tạo cấu trúc dữ liệu đồ thị.
    
    Returns:
        Tuple gồm đối tượng GraphData và thời gian (ms)
    """
    # Bắt đầu đo thời gian (perf_counter: độ chính xác cao nhất)
    start = time.perf_counter()
    
    # Tạo đối tượng GraphData rỗng với các thuộc tính
    graph = GraphData(directed=directed, weighted=weighted)
    # Nạp dữ liệu đỉnh và cạnh vào đồ thị (xây dựng cấu trúc adjacency)
    graph.load_from_edges(nodes, edges)
    
    # Tính thời gian đã trôi qua và chuyển từ giây sang milliseconds
    elapsed = (time.perf_counter() - start) * 1000  # Chuyển sang ms
    return graph, elapsed  # Trả về đồ thị và thời gian

def measure_check_edge(graph: GraphData, iterations: int = 1000) -> float: # Đo thời gian kiểm tra sự tồn tại của cạnh
    """
    Đo thời gian kiểm tra sự tồn tại của cạnh.
    Thực hiện nhiều lần để có kết quả chính xác.
    
    Returns:
        Thời gian tổng cộng (ms) cho tất cả iterations
    """
    # Lấy danh sách tất cả các đỉnh trong đồ thị
    nodes = graph.nodes
    if len(nodes) < 2:
        return 0.0  # Không đủ đỉnh để tạo cạnh
    
    # Chuẩn bị danh sách các cặp đỉnh ngẫu nhiên để kiểm tra
    # Ví dụ: [("0","5"), ("3","7"), ...] với iterations=1000 cặp
    test_pairs = [(random.choice(nodes), random.choice(nodes)) for _ in range(iterations)]
    
    # Bắt đầu đo thời gian
    start = time.perf_counter()
    for u, v in test_pairs:
        # Kiểm tra xem có cạnh từ u đến v không
        # graph.adjacency.get(u, {}) → lấy dict các đỉnh kề của u
        # v in {...} → kiểm tra v có trong dict đó không
        _ = v in graph.adjacency.get(u, {})
    elapsed = (time.perf_counter() - start) * 1000  # Chuyển sang ms
    
    return elapsed  # Trả về tổng thời gian cho 1000 lần kiểm tra

def measure_get_neighbors(graph: GraphData, iterations: int = 1000) -> float: # Đo thời gian lấy danh sách các đỉnh kề
    """
    Đo thời gian lấy danh sách các đỉnh kề.
    
    Returns:
        Thời gian tổng cộng (ms) cho tất cả iterations
    """
    # Lấy danh sách tất cả các đỉnh
    nodes = graph.nodes
    if not nodes:
        return 0.0  # Đồ thị rỗng
    
    # Chuẩn bị danh sách các đỉnh ngẫu nhiên để test
    # Ví dụ: ["3", "7", "1", ...] với iterations=1000 đỉnh
    test_nodes = [random.choice(nodes) for _ in range(iterations)]
    
    # Bắt đầu đo thời gian
    start = time.perf_counter()
    for node in test_nodes:
        # Lấy danh sách các đỉnh kề của node
        # graph.adjacency.get(node, {}) → dict {láng_giềng: trọng_số}
        # .keys() → lấy danh sách tên các láng giềng
        # list(...) → chuyển thành list
        _ = list(graph.adjacency.get(node, {}).keys())
    elapsed = (time.perf_counter() - start) * 1000  # Chuyển sang ms
    
    return elapsed  # Trả về tổng thời gian cho 1000 lần lấy danh sách kề

def measure_create_matrix(graph: GraphData) -> float: # Đo thời gian tạo ma trận kề
    """
    Đo thời gian tạo ma trận kề.
    
    Returns:
        Thời gian (ms)
    """
    # Bắt đầu đo thời gian
    start = time.perf_counter()
    # Gọi phương thức tạo ma trận kề (list of lists)
    # Ví dụ: [[0, 5, ∞], [∞, 0, 3], [2, ∞, 0]]
    _ = graph.adjacency_matrix()
    elapsed = (time.perf_counter() - start) * 1000  # Chuyển sang ms
    return elapsed  # Trả về thời gian tạo ma trận

def measure_create_adj_list(graph: GraphData) -> float: # Đo thời gian tạo danh sách kề
    """
    Đo thời gian tạo danh sách kề.
    
    Returns:
        Thời gian (ms)
    """
    # Bắt đầu đo thời gian
    start = time.perf_counter()
    # Gọi phương thức tạo danh sách kề (dict)
    # Ví dụ: {"0": ["1", "2"], "1": ["2"], "2": []}
    _ = graph.adjacency_list()
    elapsed = (time.perf_counter() - start) * 1000  # Chuyển sang ms
    return elapsed  # Trả về thời gian tạo danh sách kề

def measure_draw_time(graph: GraphData) -> float: # Đo thời gian vẽ đồ thị bằng Matplotlib + NetworkX
    """
    Đo thời gian vẽ đồ thị bằng Matplotlib + NetworkX.
    Lưu ý: Phần này phụ thuộc vào thư viện bên ngoài.
    
    Returns:
        Thời gian (ms)
    """
    try:
        # Import các thư viện cần thiết
        import networkx as nx
        import matplotlib
        matplotlib.use('Agg')  # Sử dụng backend không hiển thị (không mở cửa sổ)
        import matplotlib.pyplot as plt
        
        # Bắt đầu đo thời gian
        start = time.perf_counter()
        
        # Bước 1: Chuyển đổi GraphData sang NetworkX Graph
        nx_graph = graph.to_networkx()
        
        # Bước 2: Tính toán vị trí các đỉnh (spring layout - thuật toán lò xo)
        # seed=42 để kết quả nhất quán
        pos = nx.spring_layout(nx_graph, seed=42)
        
        # Bước 3: Vẽ đồ thị (không hiển thị, chỉ tạo trong bộ nhớ)
        fig, ax = plt.subplots(figsize=(8, 6))  # Tạo figure 8x6 inch
        nx.draw_networkx_nodes(nx_graph, pos, ax=ax, node_size=300)  # Vẽ đỉnh
        nx.draw_networkx_edges(nx_graph, pos, ax=ax)  # Vẽ cạnh
        nx.draw_networkx_labels(nx_graph, pos, ax=ax, font_size=8)  # Vẽ label
        
        plt.close(fig)  # Đóng figure để giải phóng bộ nhớ (quan trọng!)
        
        # Tính thời gian đã trôi qua
        elapsed = (time.perf_counter() - start) * 1000  # Chuyển sang ms
        return elapsed
        
    except ImportError:
        # Nếu không có NetworkX hoặc Matplotlib → trả về 0
        return 0.0

def run_single_benchmark( # Chạy benchmark cho một cấu hình đồ thị cụ thể
    n_nodes: int, 
    density: float, 
    directed: bool = False, 
    weighted: bool = False,
    include_draw: bool = True,
    seed: int = 42
) -> BenchmarkResult:
    """
    Chạy benchmark cho một cấu hình đồ thị cụ thể.
    
    Args:
        n_nodes: Số lượng đỉnh
        density: Mật độ đồ thị
        directed: Đồ thị có hướng
        weighted: Đồ thị có trọng số
        include_draw: Có đo thời gian vẽ không
        seed: Random seed
    
    Returns:
        BenchmarkResult chứa tất cả kết quả đo
    """
    # Bước 1: Tạo đồ thị ngẫu nhiên với cấu hình cho trước
    # Trả về: (danh sách đỉnh, danh sách cạnh)
    nodes, edges = generate_random_graph(n_nodes, density, directed, weighted, seed)
    
    # Bước 2: Đo thời gian tạo cấu trúc dữ liệu (GraphData + load_from_edges)
    # Trả về: (đối tượng graph, thời gian tạo)
    graph, create_time = measure_create_structure(nodes, edges, directed, weighted)
    
    # Bước 3: Đo thời gian kiểm tra cạnh (1000 lần kiểm tra ngẫu nhiên)
    # Đo hiệu năng tra cứu: v in graph.adjacency.get(u, {})
    check_edge_time = measure_check_edge(graph)
    
    # Bước 4: Đo thời gian lấy danh sách kề (1000 lần lấy ngẫu nhiên)
    # Đo hiệu năng truy xuất: graph.adjacency.get(node, {}).keys()
    get_neighbors_time = measure_get_neighbors(graph)
    
    # Bước 5: Đo thời gian tạo ma trận kề (chuyển đổi adjacency → matrix)
    # Đo hiệu năng chuyển đổi sang biểu diễn ma trận
    create_matrix_time = measure_create_matrix(graph)
    
    # Bước 6: Đo thời gian tạo danh sách kề (chuyển đổi adjacency → adj_list)
    # Đo hiệu năng chuyển đổi sang biểu diễn danh sách
    create_adj_list_time = measure_create_adj_list(graph)
    
    # Bước 7: Đo thời gian vẽ (chỉ với đồ thị nhỏ/vừa để tránh quá lâu)
    draw_time = 0.0
    if include_draw and n_nodes <= 200:  # Giới hạn ≤200 đỉnh
        draw_time = measure_draw_time(graph)
    
    # Tổng hợp tất cả kết quả vào đối tượng BenchmarkResult
    return BenchmarkResult(
        n_nodes=n_nodes,
        density=density,
        n_edges=graph.edge_count(),  # Số cạnh thực tế (có thể khác target)
        directed=directed,
        weighted=weighted,
        create_structure_time=create_time,
        check_edge_time=check_edge_time,
        get_neighbors_time=get_neighbors_time,
        create_matrix_time=create_matrix_time,
        create_adj_list_time=create_adj_list_time,
        draw_time=draw_time
    )

def run_full_benchmark( # Chạy benchmark đầy đủ với nhiều cấu hình khác nhau
    sizes: List[int] = None,
    densities: List[float] = None,
    include_draw: bool = True
) -> List[BenchmarkResult]:
    """
    Chạy benchmark đầy đủ với nhiều cấu hình khác nhau.
    
    Args:
        sizes: Danh sách số lượng đỉnh để test
        densities: Danh sách mật độ để test
        include_draw: Có đo thời gian vẽ không
    
    Returns:
        Danh sách các BenchmarkResult
    """
    # Thiết lập giá trị mặc định nếu không được cung cấp
    if sizes is None:
        sizes = [50, 200, 500]  # Đồ thị nhỏ, vừa, lớn
    if densities is None:
        densities = [0.1, 0.3, 0.5]  # Thưa (10%), vừa (30%), dày (50%)
    
    # Danh sách lưu kết quả tất cả các test
    results = []
    print()
    
    # Vòng lặp qua tất cả các kết hợp (size, density)
    # Ví dụ: (50, 0.1), (50, 0.3), (50, 0.5), (200, 0.1), ...
    for n in sizes:
        for d in densities:
            # In thông báo đang test (không xuống dòng, flush ngay)
            print(f"Đang test: {n} đỉnh, mật độ {d*100:.0f}%...", end=" ", flush=True)
            
            # Chạy benchmark cho cấu hình này
            result = run_single_benchmark(
                n_nodes=n, 
                density=d, 
                directed=False,  # Mặc định: vô hướng
                weighted=False,  # Mặc định: không trọng số
                include_draw=include_draw
            )
            # Thêm kết quả vào danh sách
            results.append(result)
            
            # In thông báo hoàn thành (có số cạnh thực tế)
            print(f"Hoàn thành ({result.n_edges} cạnh)")
    
    print()
    return results  # Trả về danh sách tất cả kết quả

def print_results_table(results: List[BenchmarkResult]) -> None: # In kết quả dưới dạng bảng
    """In kết quả dưới dạng bảng đẹp."""
    
    print("=" * 130)
    print("  KẾT QUẢ ĐÁNH GIÁ HIỆU NĂNG")
    print("=" * 130)
    print()
    
    # Header
    print(f"{'Đỉnh':>6} | {'Mật độ':>8} | {'Số cạnh':>8} | {'Tạo CTDL':>12} | {'Check cạnh':>12} | {'Lấy kề':>12} | {'Ma trận kề':>12} | {'DS kề':>12} | {'Vẽ':>10}")
    print(f"{'':>6} | {'':>8} | {'':>8} | {'(ms)':>12} | {'(1000x, ms)':>12} | {'(1000x, ms)':>12} | {'(ms)':>12} | {'(ms)':>12} | {'(ms)':>10}")
    print("-" * 130)
    
    for r in results:
        draw_str = f"{r.draw_time:.2f}" if r.draw_time > 0 else "N/A"
        print(f"{r.n_nodes:>6} | {r.density*100:>7.0f}% | {r.n_edges:>8} | {r.create_structure_time:>12.3f} | {r.check_edge_time:>12.3f} | {r.get_neighbors_time:>12.3f} | {r.create_matrix_time:>12.3f} | {r.create_adj_list_time:>12.3f} | {draw_str:>10}")
    
    print("-" * 130)
    print()

def print_analysis(results: List[BenchmarkResult]) -> None: # In phân tích kết quả
    """In phân tích kết quả."""
    
    print("=" * 90)
    print("  PHÂN TÍCH KẾT QUẢ")
    print("=" * 90)
    print()
    
    # 1. Phân tích theo kích thước
    print("PHÂN TÍCH THEO KÍCH THƯỚC ĐỒ THỊ:")
    print("-" * 60)
    
    sizes = sorted(set(r.n_nodes for r in results))
    for size in sizes:
        size_results = [r for r in results if r.n_nodes == size]
        avg_create = sum(r.create_structure_time for r in size_results) / len(size_results)
        avg_matrix = sum(r.create_matrix_time for r in size_results) / len(size_results)
        print(f"  - {size} đỉnh: Tạo CTDL TB = {avg_create:.3f} ms, Ma trận kề TB = {avg_matrix:.3f} ms")
    
    print()
    
    # 2. Phân tích theo mật độ
    print("PHÂN TÍCH THEO MẬT ĐỘ:")
    print("-" * 60)
    
    densities = sorted(set(r.density for r in results))
    for density in densities:
        density_results = [r for r in results if r.density == density]
        avg_create = sum(r.create_structure_time for r in density_results) / len(density_results)
        avg_edges = sum(r.n_edges for r in density_results) / len(density_results)
        print(f"  - Mật độ {density*100:.0f}%: Số cạnh TB = {avg_edges:.0f}, Tạo CTDL TB = {avg_create:.3f} ms")
    
    print()
    
    # 3. So sánh thời gian xử lý vs vẽ
    print("SO SÁNH THỜI GIAN XỬ LÝ DỮ LIỆU vs VẼ ĐỒ THỊ:")
    print("-" * 60)
    
    for r in results:
        if r.draw_time > 0:
            total_process = r.create_structure_time + r.create_matrix_time + r.create_adj_list_time
            ratio = r.draw_time / total_process if total_process > 0 else 0
            print(f"  • {r.n_nodes} đỉnh, {r.density*100:.0f}%: Xử lý = {total_process:.2f} ms, Vẽ = {r.draw_time:.2f} ms (gấp {ratio:.1f}x)")
    
    print()
    
def export_results_to_file(results: List[BenchmarkResult], filepath: str = None) -> str: # Xuất kết quả benchmark ra file văn bản
    """
    Xuất kết quả benchmark ra file văn bản.
    
    Returns:
        Đường dẫn file đã lưu
    """
    if filepath is None:
        filepath = Path(__file__).parent / "benchmark_results.txt"
    
    lines = []
    # Bảng kết quả
    lines.append("BẢNG KẾT QUẢ CHI TIẾT:")
    lines.append("-" * 110)
    lines.append(f"{'Đỉnh':>6} | {'Mật độ':>8} | {'Số cạnh':>8} | {'Tạo CTDL':>12} | {'Check cạnh':>12} | {'Lấy kề':>12} | {'Ma trận kề':>12} | {'DS kề':>12}")
    lines.append(f"{'':>6} | {'':>8} | {'':>8} | {'(ms)':>12} | {'(1000x, ms)':>12} | {'(1000x, ms)':>12} | {'(ms)':>12} | {'(ms)':>12}")
    lines.append("-" * 110)
    
    for r in results:
        lines.append(f"{r.n_nodes:>6} | {r.density*100:>7.0f}% | {r.n_edges:>8} | {r.create_structure_time:>12.3f} | {r.check_edge_time:>12.3f} | {r.get_neighbors_time:>12.3f} | {r.create_matrix_time:>12.3f} | {r.create_adj_list_time:>12.3f}")
    
    lines.append("-" * 110)
    lines.append("")
    
    # Ghi file
    Path(filepath).write_text("\n".join(lines), encoding="utf-8")
    return str(filepath)

def main(): # Hàm chính để chạy benchmark
    """Hàm chính để chạy benchmark."""
    print()
    print("Bắt đầu đánh giá hiệu năng")
    print()
    
    # Chạy benchmark với các cấu hình mặc định
    results = run_full_benchmark(
        sizes=[50, 200, 500],
        densities=[0.1, 0.3, 0.5],
        include_draw=True
    )
    
    # In kết quả
    print_results_table(results)
    
    # In phân tích
    print_analysis(results)
    
    # Xuất file
    filepath = export_results_to_file(results)
    print(f"Đã lưu kết quả vào: {filepath}")
    print()

if __name__ == "__main__":
    main()
