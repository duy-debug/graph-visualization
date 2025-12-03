from __future__ import annotations
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx
from .graph_data import GraphData
from .graph_io import (
    export_graph_to_file,
    load_karate_club,
    read_graph_from_file,
    read_graph_from_text,
)
class GraphApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Mô phỏng đồ thị")
        self.geometry("1200x800")
        try:
            self.state("zoomed")
        except tk.TclError:
            self.attributes("-zoomed", True)
        self.graph = GraphData()
        # Biến cho tính năng kéo thả đỉnh
        self.pos = None  # Vị trí các đỉnh
        self.dragging = False  # Đang kéo đỉnh
        self.selected_node = None  # Đỉnh được chọn
        self.drag_offset = None  # Độ lệch giữa điểm click và tâm đỉnh khi kéo
        # Biến cho highlight bằng click
        self.highlighted_nodes = set()  # Các đỉnh được highlight
        self.highlighted_edges = set()  # Các cạnh được highlight (u, v
        self._build_widgets()
        self._draw_graph()
    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def _build_widgets(self) -> None:
        main = ttk.Frame(self, padding=10)
        main.pack(fill=tk.BOTH, expand=True)
        self.options_var = {
            "directed": tk.BooleanVar(value=False),
            "weighted": tk.BooleanVar(value=False),
        }
        options_frame = ttk.LabelFrame(main, text="Dữ liệu nhập vào", padding=5)
        options_frame.pack(fill=tk.X, pady=2)
        ttk.Label(
            options_frame,
            text="Số lượng đỉnh",
        ).grid(row=0, column=0, sticky=tk.W, padx=5, pady=1)
        self.nodes_entry = ttk.Entry(options_frame, width=40)
        self.nodes_entry.grid(row=1, column=0, sticky=tk.EW, padx=5)
        ttk.Label(options_frame, text="Danh sách cạnh").grid(
            row=2, column=0, sticky=tk.W, padx=5, pady=1
        )
        # Text widget với scrollbar cho danh sách cạnh (height giảm từ 6 xuống 4)
        edges_frame = ttk.Frame(options_frame)
        edges_frame.grid(row=3, column=0, sticky=tk.EW, padx=5)
        self.edges_entry = tk.Text(edges_frame, height=3, width=40)
        edges_scrollbar = ttk.Scrollbar(edges_frame, orient=tk.VERTICAL, command=self.edges_entry.yview)
        self.edges_entry.configure(yscrollcommand=edges_scrollbar.set)
        self.edges_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        edges_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # Auto-update khi thay đổi nội dung danh sách cạnh
        self.edges_entry.bind('<KeyRelease>', lambda e: self._auto_update_graph())
        check_frame = ttk.Frame(options_frame)
        check_frame.grid(row=0, column=1, rowspan=4, sticky=tk.NE, padx=10)
        ttk.Checkbutton(
            check_frame,
            text="Đồ thị có hướng",
            variable=self.options_var["directed"],
            command=self._on_option_change,
        ).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(
            check_frame,
            text="Đồ thị có trọng số",
            variable=self.options_var["weighted"],
            command=self._on_option_change,
        ).pack(anchor=tk.W, pady=2)
        
        # Label hiển thị lỗi (đặt ở dòng riêng để không làm dịch chuyển checkbox)
        self.error_label_var = tk.StringVar(value="")
        self.error_label = ttk.Label(
            options_frame, 
            textvariable=self.error_label_var, 
            foreground="red",
            wraplength=600
        )
        self.error_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5, pady=(0, 3))

        btn_frame = ttk.Frame(options_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, sticky=tk.EW, pady=3)
        ttk.Button(btn_frame, text="Đọc file", command=self._import_from_file).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Tải Karate Club", command=self._load_karate).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Xuất file", command=self._export_graph).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Reset", command=self._reset_graph).pack(
            side=tk.LEFT, padx=5
        )
        # hiển thị cấu trúc + đồ thị trong paned window
        paned = ttk.PanedWindow(main, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, pady=2)
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        matrix_frame = ttk.LabelFrame(left_panel, text="Ma trận kề")
        matrix_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.matrix_table = ttk.Treeview(
            matrix_frame, columns=[], show="headings", height=8
        )
        self.matrix_table.pack(fill=tk.BOTH, expand=True)
        list_frame = ttk.LabelFrame(left_panel, text="Danh sách kề")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        self.adj_list_text = tk.Text(list_frame, height=10, state=tk.DISABLED)
        self.adj_list_text.pack(fill=tk.BOTH, expand=True)
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=1)
        # Thao tác thêm/xóa - Di chuyển lên đầu
        crud_frame = ttk.LabelFrame(right_panel, text="Thao tác thêm/xóa")
        crud_frame.pack(fill=tk.X, pady=(0, 5), padx=5)

        # node controls
        ttk.Label(crud_frame, text="Đỉnh:").grid(row=0, column=0, padx=5, pady=2)
        self.node_name_entry = ttk.Entry(crud_frame, width=10)
        self.node_name_entry.grid(row=0, column=1, padx=5)
        ttk.Button(crud_frame, text="Thêm đỉnh", command=self._add_vertex).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(crud_frame, text="Xóa đỉnh", command=self._remove_vertex).grid(
            row=0, column=3, padx=5
        )
        # edge controls
        ttk.Label(crud_frame, text="Cạnh").grid(row=1, column=0, padx=5, pady=2)
        self.edge_u_entry = ttk.Entry(crud_frame, width=8)
        self.edge_u_entry.grid(row=1, column=1, padx=5)
        self.edge_v_entry = ttk.Entry(crud_frame, width=8)
        self.edge_v_entry.grid(row=1, column=2, padx=5)
        self.edge_w_entry = ttk.Entry(crud_frame, width=8, state=tk.DISABLED)
        self.edge_w_entry.grid(row=1, column=3, padx=5)
        ttk.Button(crud_frame, text="Thêm cạnh", command=self._add_edge).grid(
            row=1, column=4, padx=5
        )
        ttk.Button(crud_frame, text="Xóa cạnh", command=self._remove_edge).grid(
            row=1, column=5, padx=5
        )
        # Biểu diễn trực quan - Sau thao tác thêm/xóa
        plot_frame = ttk.LabelFrame(right_panel, text="Biểu diễn trực quan")
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        self.figure = Figure(figsize=(5, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Kết nối event handlers cho kéo thả đỉnh
        self.canvas.mpl_connect('button_press_event', self._on_mouse_press)
        self.canvas.mpl_connect('button_release_event', self._on_mouse_release)
        self.canvas.mpl_connect('motion_notify_event', self._on_mouse_motion)
        highlight_frame = ttk.Frame(right_panel)
        highlight_frame.pack(fill=tk.X, pady=5, padx=5)
        # Cấu hình grid để density label nằm bên phải
        highlight_frame.grid_columnconfigure(1, weight=1)
        ttk.Label(highlight_frame, text="Highlight đỉnh").grid(
            row=0, column=0, sticky=tk.W, padx=5
        )
        self.highlight_nodes_entry = ttk.Entry(highlight_frame, width=25)
        self.highlight_nodes_entry.grid(row=0, column=1, padx=5, sticky=tk.EW)
        # Auto-update khi thay đổi nội dung
        self.highlight_nodes_entry.bind('<KeyRelease>', lambda e: self._update_highlights_from_inputs())
        ttk.Label(highlight_frame, text="Highlight cạnh").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=2
        )
        self.highlight_edges_entry = ttk.Entry(highlight_frame, width=25)
        self.highlight_edges_entry.grid(row=1, column=1, padx=5, sticky=tk.EW)
        # Auto-update khi thay đổi nội dung
        self.highlight_edges_entry.bind('<KeyRelease>', lambda e: self._update_highlights_from_inputs())
        # Density label - đặt bên phải highlight controls
        self.density_label_var = tk.StringVar(value="Mật độ: ")
        ttk.Label(highlight_frame, textvariable=self.density_label_var, font=('TkDefaultFont', 10, 'bold')).grid(
            row=0, column=2, rowspan=2, sticky=tk.E, padx=15
        )
    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _parse_node_count(self) -> int:
        """Đọc số lượng đỉnh từ ô nhập"""
        text = self.nodes_entry.get().strip()
        if not text:
            return 0
        try:
            count = int(text)
            if count < 0:
                raise ValueError("Số lượng đỉnh phải >= 0")
            return count
        except ValueError:
            raise ValueError("Số lượng đỉnh phải là một số nguyên hợp lệ.")

    def _extract_nodes_from_edges(self) -> set[str]:
        """Trích xuất tất cả các đỉnh từ danh sách cạnh (kể cả dòng chỉ có 1 đỉnh)"""
        nodes = set()
        for raw in self.edges_entry.get("1.0", tk.END).strip().splitlines():
            raw = raw.strip()
            if not raw:
                continue
            parts = raw.split()
            if len(parts) >= 2:
                nodes.add(parts[0])
                nodes.add(parts[1])
            elif len(parts) == 1:
                nodes.add(parts[0])
        return nodes
    def _parse_edges(
        self,
        allowed_nodes: set[str] | None = None,
        weighted_flag: bool | None = None,
    ) -> list[tuple[str, str, float]]:
        """Parse danh sách cạnh. allowed_nodes có thể None để chấp nhận mọi đỉnh."""
        if weighted_flag is None:
            weighted_flag = self.options_var["weighted"].get()
        edges: list[tuple[str, str, float]] = []
        line_no = 0
        for raw in self.edges_entry.get("1.0", tk.END).strip().splitlines():
            raw = raw.strip()
            line_no += 1
            if not raw:
                continue
            parts = raw.split()
            if len(parts) == 1:
                # Dòng chỉ có một đỉnh, dùng để khai báo đỉnh đơn lẻ
                continue
            if len(parts) < 2:
                raise ValueError(f"Dòng {line_no}: cần tối thiểu 1 đỉnh hoặc 1 cạnh.")
            u, v = parts[:2]
            # Chỉ kiểm tra allowed_nodes nếu được chỉ định (không bắt buộc)
            if allowed_nodes is not None and (u not in allowed_nodes or v not in allowed_nodes):
                raise ValueError(
                    f"Dòng {line_no}: đỉnh '{u}' hoặc '{v}' không nằm trong danh sách đã nhập."
                )
            # Xử lý trọng số
            if weighted_flag:
                if len(parts) == 3:
                    try:
                        weight = float(parts[2])
                    except ValueError:
                        raise ValueError(f"Dòng {line_no}: trọng số '{parts[2]}' không hợp lệ.")
                elif len(parts) == 2:
                    weight = 0.0  # mặc định 0 nếu không nhập trọng số
                else:
                    raise ValueError(
                        f"Dòng {line_no}: định dạng cạnh không hợp lệ (chỉ hỗ trợ 'u v' hoặc 'u v w')."
                    )
            else:
                if len(parts) >= 3:
                    raise ValueError(
                        f"Dòng {line_no}: đồ thị không trọng số, không được nhập trọng số."
                    )
                weight = 1.0
            edges.append((u, v, weight))
        return edges
    def _update_graph(self) -> None:
        try:
            # Trích xuất tất cả đỉnh từ danh sách cạnh (chấp nhận mọi loại: số, chữ, ký tự đặc biệt)
            edges_nodes = self._extract_nodes_from_edges()
            if not edges_nodes:
                raise ValueError("Vui lòng nhập ít nhất một cạnh (ô danh sách cạnh).")
            # Đọc số lượng đỉnh ban đầu (nếu có)
            initial_count = self._parse_node_count()
            # Sắp xếp danh sách đỉnh để có thứ tự nhất quán
            # Sắp xếp theo thứ tự từ điển (chấp nhận mọi loại đỉnh: số, chữ, ký tự đặc biệt)
            nodes_list = sorted(edges_nodes)
            # Tự động cập nhật số lượng đỉnh dựa trên số đỉnh thực tế tìm được
            actual_count = len(nodes_list)
            self.nodes_entry.delete(0, tk.END)
            self.nodes_entry.insert(0, str(actual_count))
            # Parse edges với danh sách đỉnh thực tế từ cạnh
            edges = self._parse_edges(None)  # Không kiểm tra allowed_nodes nữa
            weighted_option = self.options_var["weighted"].get()
            if not nodes_list:
                raise ValueError("Cần ít nhất 1 đỉnh")
            g = GraphData(
                directed=self.options_var["directed"].get(),
                weighted=weighted_option,
            )
            g.load_from_edges(nodes_list, edges)
            self.graph = g
            self.pos = None  # Reset vị trí đỉnh
            self._refresh_views()
        except ValueError as exc:
            messagebox.showerror("Lỗi nhập liệu", str(exc))
    def _auto_update_graph(self) -> None:
        """Tự động cập nhật đồ thị khi nhập danh sách cạnh"""
        try:
            # Xóa thông báo lỗi cũ
            self.error_label_var.set("")
            # Trích xuất tất cả đỉnh từ danh sách cạnh
            edges_nodes = self._extract_nodes_from_edges()
            if not edges_nodes:
                # Nếu không có cạnh nào, reset đồ thị
                self.graph = GraphData(
                    directed=self.options_var["directed"].get(),
                    weighted=self.options_var["weighted"].get(),
                )
                self.pos = None  # Reset vị trí đỉnh
                self._refresh_views()
                return
            # Sắp xếp danh sách đỉnh
            nodes_list = sorted(edges_nodes)
            # Tự động cập nhật số lượng đỉnh
            actual_count = len(nodes_list)
            current_count = self.nodes_entry.get().strip()
            if current_count != str(actual_count):
                self.nodes_entry.delete(0, tk.END)
                self.nodes_entry.insert(0, str(actual_count))
            # Tự động phát hiện trọng số và validate
            has_weight = False
            edges_text = self.edges_entry.get("1.0", tk.END).strip()
            line_num = 0
            for line in edges_text.splitlines():
                line = line.strip()
                line_num += 1
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 3:
                    # Kiểm tra trọng số có hợp lệ không
                    try:
                        float(parts[2])
                        has_weight = True
                    except ValueError:
                        raise ValueError(f"Lỗi dòng {line_num}: Trọng số '{parts[2]}' không phải là số hợp lệ")
            # Tự động tick/untick checkbox trọng số
            if has_weight != self.options_var["weighted"].get():
                self.options_var["weighted"].set(has_weight)
                # Toggle ô trọng số
                if has_weight:
                    self.edge_w_entry.config(state=tk.NORMAL)
                else:
                    self.edge_w_entry.config(state=tk.DISABLED)
                    self.edge_w_entry.delete(0, tk.END)
            # Parse edges với trọng số mặc định là 0 nếu có ít nhất 1 cạnh có trọng số
            edges = self._parse_edges(None, weighted_flag=has_weight)
            # Tạo đồ thị mới
            g = GraphData(
                directed=self.options_var["directed"].get(),
                weighted=has_weight,
            )
            g.load_from_edges(nodes_list, edges)
            self.graph = g
            self.pos = None  # Reset vị trí đỉnh khi cấu trúc đồ thị thay đổi
            # Cập nhật hiển thị (không cập nhật ô nhập liệu để tránh xóa cursor)
            self._update_matrix()
            self._update_adj_list()
            self._draw_graph()
            density = self.graph.density()
            label = f"Mật độ: {density:.3f} ({self.graph.density_label()})"
            self.density_label_var.set(label)
        except ValueError as e:
            # Hiển thị lỗi trong label màu đỏ
            self.error_label_var.set(str(e))
    def _on_option_change(self) -> None:
        old_directed = self.graph.directed
        new_directed = self.options_var["directed"].get()
        self.graph.directed = new_directed
        self.graph.weighted = self.options_var["weighted"].get()
        # Nếu chuyển từ vô hướng sang có hướng, cần xóa các cạnh ngược
        if not old_directed and new_directed:
            # Lấy danh sách cạnh từ ô nhập
            edges_text = self.edges_entry.get("1.0", tk.END).strip()
            if edges_text:
                # Parse lại edges từ input để biết thứ tự ban đầu
                try:
                    edges_nodes = self._extract_nodes_from_edges()
                    if edges_nodes:
                        nodes_list = sorted(edges_nodes)
                        edges = self._parse_edges(None, weighted_flag=self.graph.weighted)
                        # Tạo lại đồ thị chỉ với các cạnh theo thứ tự nhập
                        g = GraphData(directed=True, weighted=self.graph.weighted)
                        g.load_from_edges(nodes_list, edges)
                        self.graph = g
                        self.pos = None
                except:
                    pass  # Nếu có lỗi, giữ nguyên
        # Toggle ô trọng số dựa trên weighted option
        if self.graph.weighted:
            self.edge_w_entry.config(state=tk.NORMAL)
        else:
            self.edge_w_entry.config(state=tk.DISABLED)
            self.edge_w_entry.delete(0, tk.END)  # Xóa giá trị cũ
        # Chỉ cập nhật hiển thị mà KHÔNG cập nhật ô nhập liệu
        self._update_matrix()
        self._update_adj_list()
        self._draw_graph()
        density = self.graph.density()
        label = f"Mật độ: {density:.3f} ({self.graph.density_label()})"
        self.density_label_var.set(label)
    def _import_from_file(self) -> None:
        file_path = filedialog.askopenfilename(
            title="Chọn file đồ thị",
            filetypes=[("Text", "*.txt"), ("All files", "*.*")],
        )
        if not file_path:
            return
        try:
            # Đọc file (bỏ qua tham số directed/weighted vì sẽ tự động phát hiện)
            self.graph = read_graph_from_file(file_path)
            
            # Tự động cập nhật các checkbox theo dữ liệu đọc được
            self.options_var["directed"].set(self.graph.directed)
            self.options_var["weighted"].set(self.graph.weighted)
            
            # Toggle ô trọng số dựa trên weighted option
            if self.graph.weighted:
                self.edge_w_entry.config(state=tk.NORMAL)
            else:
                self.edge_w_entry.config(state=tk.DISABLED)
                self.edge_w_entry.delete(0, tk.END)
            
            self.pos = None  # Reset vị trí đỉnh
            self._refresh_views()
            self.nodes_entry.delete(0, tk.END)
            self.nodes_entry.insert(0, str(len(self.graph.nodes)))
            self.edges_entry.delete("1.0", tk.END)
            edges_lines = []
            for u, nbrs in self.graph.adjacency.items():
                for v, w in nbrs.items():
                    if self.graph.directed or u <= v:
                        if self.graph.weighted:
                            edges_lines.append(f"{u} {v} {w}")
                        else:
                            edges_lines.append(f"{u} {v}")
            self.edges_entry.insert("1.0", "\n".join(edges_lines))
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Không đọc được file", str(exc))
    def _export_graph(self) -> None:
        """Xuất cấu trúc đồ thị hiện tại ra file .txt bằng hộp thoại lưu file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text", "*.txt")],
            title="Lưu cấu trúc đồ thị",
        )
        if not file_path:
            return
        export_graph_to_file(self.graph, file_path)
        messagebox.showinfo("Hoàn tất", f"Đã lưu vào {file_path}")
    def _load_karate(self) -> None:
        """Tải đồ thị Karate Club mẫu để demo, thay thế đồ thị hiện tại."""
        self.graph = load_karate_club(directed=self.options_var["directed"].get())
        self.pos = None  # Reset vị trí đỉnh
        self._refresh_views()
        self.nodes_entry.delete(0, tk.END)
        self.nodes_entry.insert(0, str(len(self.graph.nodes)))
        edges_text = []
        for u, nbrs in self.graph.adjacency.items():
            for v in nbrs.keys():
                if self.graph.directed or u <= v:
                    edges_text.append(f"{u} {v}")
        self.edges_entry.delete("1.0", tk.END)
        self.edges_entry.insert("1.0", "\n".join(edges_text))
    def _add_vertex(self) -> None:
        name = self.node_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đỉnh cần thêm")
            return
        if name in self.graph.nodes:
            messagebox.showwarning("Trùng tên", "Đỉnh đã tồn tại")
            return
        self.graph.add_node(name)
        self._refresh_views()
    def _remove_vertex(self) -> None:
        name = self.node_name_entry.get().strip()
        if not name:
            messagebox.showwarning("Thông báo", "Vui lòng nhập tên đỉnh cần xóa")
            return
        self.graph.remove_node(name)
        # Xóa highlight liên quan đến đỉnh vừa xóa
        if name in self.highlighted_nodes:
            self.highlighted_nodes.remove(name)
        # Xóa các cạnh có liên quan tới đỉnh vừa xóa khỏi danh sách highlight cạnh
        edges_to_remove = set()
        for u, v in self.highlighted_edges:
            if u == name or v == name:
                edges_to_remove.add((u, v))
        for edge in edges_to_remove:
            self.highlighted_edges.remove(edge)
        # Đồng bộ lại ô nhập highlight và giao diện
        self._sync_highlight_inputs()
        self._refresh_views()
    def _add_edge(self) -> None:
        u = self.edge_u_entry.get().strip()
        v = self.edge_v_entry.get().strip()
        if not u or not v:
            messagebox.showwarning("Thông báo", "Vui lòng nhập 2 đỉnh để thêm cạnh")
            return
        # Kiểm tra cạnh trùng CHỈ khi đồ thị KHÔNG có trọng số
        if not self.graph.weighted:
            if u in self.graph.adjacency and v in self.graph.adjacency.get(u, {}):
                messagebox.showwarning(
                    "Cạnh đã tồn tại", 
                    f"Cạnh giữa '{u}' và '{v}' đã tồn tại trong đồ thị"
                )
                return
        w_text = self.edge_w_entry.get().strip()
        # Validate trọng số
        if w_text and self.graph.weighted:
            try:
                weight = float(w_text)
            except ValueError:
                messagebox.showerror(
                    "Trọng số không hợp lệ", 
                    f"Trọng số '{w_text}' không phải là số hợp lệ"
                )
                return
        else:
            weight = 1.0
        # Thêm hoặc cập nhật cạnh (ghi đè nếu đã tồn tại và có trọng số)
        self.graph.add_edge(u, v, weight)
        self._refresh_views()
    def _remove_edge(self) -> None:
        u = self.edge_u_entry.get().strip()
        v = self.edge_v_entry.get().strip()
        if not u or not v:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập đỉnh u và v")
            return
        self.graph.remove_edge(u, v)
        # Xóa highlight cạnh tương ứng (xét cả hai chiều nếu đồ thị vô hướng)
        edges_to_remove = set()
        if self.graph.directed:
            if (u, v) in self.highlighted_edges:
                edges_to_remove.add((u, v))
        else:
            for edge in self.highlighted_edges:
                x, y = edge
                if (x == u and y == v) or (x == v and y == u):
                    edges_to_remove.add(edge)
        for edge in edges_to_remove:
            self.highlighted_edges.remove(edge)
        # Đồng bộ lại ô nhập highlight và giao diện
        self._sync_highlight_inputs()
        self._refresh_views()
    def _reset_graph(self) -> None:
        """Reset tất cả dữ liệu về trạng thái ban đầu"""
        # Reset các options về False (bỏ dấu tích trong checkbox)
        self.options_var["directed"].set(False)
        self.options_var["weighted"].set(False)
        # Reset đồ thị
        self.graph = GraphData(
            directed=False,
            weighted=False,
        )
        self.pos = None  # Reset vị trí đỉnh
        # Xóa tất cả các entry fields
        self.nodes_entry.delete(0, tk.END)
        self.edges_entry.delete("1.0", tk.END)
        self.highlight_nodes_entry.delete(0, tk.END)
        self.node_name_entry.delete(0, tk.END)
        self.edge_u_entry.delete(0, tk.END)
        self.edge_v_entry.delete(0, tk.END)
        self.edge_w_entry.delete(0, tk.END)
        # Xóa thông báo lỗi
        self.error_label_var.set("")
        # Xóa highlight
        self._clear_highlights()
        # Refresh views
        self._refresh_views()
    def _clear_highlights(self) -> None:
        """Xóa nội dung các ô highlight."""
        # Xóa trạng thái highlight nội bộ
        self.highlighted_nodes.clear()
        self.highlighted_edges.clear()
        # Xóa nội dung các ô nhập
        self.highlight_nodes_entry.delete(0, tk.END)
        self.highlight_edges_entry.delete(0, tk.END)
    # ------------------------------------------------------------------
    # Refresh UI
    # ------------------------------------------------------------------
    def _update_input_fields(self) -> None:
        """Cập nhật các ô nhập liệu để đồng bộ với đồ thị hiện tại"""
        # Cập nhật số lượng đỉnh (để trống nếu không có đỉnh)
        self.nodes_entry.delete(0, tk.END)
        if len(self.graph.nodes) > 0:
            self.nodes_entry.insert(0, str(len(self.graph.nodes)))
        # Cập nhật danh sách cạnh và đỉnh đơn lẻ
        self.edges_entry.delete("1.0", tk.END)
        edges_lines = []
        # Thêm các cạnh
        for u, nbrs in self.graph.adjacency.items():
            for v, w in nbrs.items():
                # Tránh trùng lặp với đồ thị vô hướng
                if self.graph.directed or u <= v:
                    if self.graph.weighted:
                        edges_lines.append(f"{u} {v} {w:g}")
                    else:
                        edges_lines.append(f"{u} {v}")
        # Thêm các đỉnh đơn lẻ (không có cạnh)
        for node in self.graph.nodes:
            if not self.graph.adjacency.get(node, {}):
                edges_lines.append(node)
        self.edges_entry.insert("1.0", "\n".join(edges_lines))
    def _refresh_views(self) -> None:
        self._update_matrix()
        self._update_adj_list()
        self._update_input_fields()  # Tự động cập nhật ô nhập liệu
        self._draw_graph()
        density = self.graph.density()
        label = f"Mật độ: {density:.3f} ({self.graph.density_label()})"
        self.density_label_var.set(label)
    def _update_matrix(self) -> None:
        matrix = self.graph.adjacency_matrix()
        # Xóa tất cả columns và rows cũ
        for col in self.matrix_table["columns"]:
            self.matrix_table.heading(col, text="")
            self.matrix_table.column(col, width=70)
        self.matrix_table.delete(*self.matrix_table.get_children())
        # Nếu đồ thị rỗng, không hiển thị gì
        if len(self.graph.nodes) == 0:
            self.matrix_table["columns"] = []
            return
        # Hiển thị ma trận kề bình thường
        columns = ["#"] + self.graph.nodes
        self.matrix_table["columns"] = columns
        for col in columns:
            self.matrix_table.heading(col, text=col)
            self.matrix_table.column(col, width=60, anchor=tk.CENTER)
        for idx, row in enumerate(matrix):
            values = [self.graph.nodes[idx]]
            u = self.graph.nodes[idx]
            for col_idx, val in enumerate(row):
                if self.graph.weighted:
                    nbr = self.graph.nodes[col_idx]
                    weight = self.graph.adjacency.get(u, {}).get(nbr)
                    if weight is None:
                        values.append("INF")
                    else:
                        values.append(f"{weight:g}")
                else:
                    values.append(f"{val:g}")
            self.matrix_table.insert("", tk.END, values=values)
    def _update_adj_list(self) -> None:
        adj_list = self.graph.adjacency_list()
        self.adj_list_text.configure(state=tk.NORMAL)
        self.adj_list_text.delete("1.0", tk.END)
        lines = []
        arrow = "→"
        for node, neighbors in adj_list.items():
            if neighbors:
                lines.append(f"{node} {arrow} {', '.join(neighbors)}")
            else:
                lines.append(f"{node} {arrow} ∅")
        self.adj_list_text.insert("1.0", "\n".join(lines))
        self.adj_list_text.configure(state=tk.DISABLED)
    def _parse_highlights(self):
        """Trả về danh sách nodes và edges được highlight từ internal state"""
        return list(self.highlighted_nodes), list(self.highlighted_edges)
    def _sync_highlight_inputs(self):
        """Đồng bộ highlight input boxes với internal state"""
        # Sync nodes
        self.highlight_nodes_entry.delete(0, tk.END)
        if self.highlighted_nodes:
            self.highlight_nodes_entry.insert(0, ','.join(sorted(self.highlighted_nodes)))
        # Sync edges
        self.highlight_edges_entry.delete(0, tk.END)
        if self.highlighted_edges:
            edge_strs = [f"{u}-{v}" for u, v in sorted(self.highlighted_edges)]
            self.highlight_edges_entry.insert(0, ';'.join(edge_strs))
    def _update_highlights_from_inputs(self):
        """Đọc từ ô input highlight và cập nhật lại trạng thái highlight nội bộ."""
        # Parse highlight nodes: ngăn cách bởi dấu phẩy hoặc khoảng trắng
        raw_nodes = self.highlight_nodes_entry.get().strip()
        new_nodes = set()
        if raw_nodes:
            for part in raw_nodes.replace(';', ',').split(','):
                name = part.strip()
                if name:
                    new_nodes.add(name)
        # Chỉ giữ lại các đỉnh có thật trong đồ thị
        self.highlighted_nodes = {n for n in new_nodes if n in self.graph.nodes}
        # Parse highlight edges: định dạng "u-v" hoặc ngăn cách bởi ; , khoảng trắng
        raw_edges = self.highlight_edges_entry.get().strip()
        new_edges = set()
        if raw_edges:
            # Thay ; bằng , để dễ split
            tmp = raw_edges.replace(';', ',')
            for part in tmp.split(','):
                part = part.strip()
                if not part:
                    continue
                # Cho phép dùng "u v" hoặc "u-v"
                if '-' in part:
                    u, v = part.split('-', 1)
                else:
                    pieces = part.split()
                    if len(pieces) != 2:
                        continue
                    u, v = pieces
                u = u.strip()
                v = v.strip()
                if not u or not v:
                    continue
                # Chỉ highlight cạnh nếu hai đỉnh tồn tại
                if u in self.graph.nodes and v in self.graph.nodes:
                    new_edges.add((u, v))
        self.highlighted_edges = new_edges
        # Sau khi cập nhật trạng thái highlight nội bộ, vẽ lại đồ thị
        self._draw_graph()
    def _draw_graph(self) -> None:
        self.ax.clear()
        nx_graph = self.graph.to_networkx()
        # Chỉ tính toán lại layout nếu chưa có hoặc số đỉnh thay đổi
        if self.pos is None or set(self.pos.keys()) != set(nx_graph.nodes()):
            self.pos = nx.spring_layout(nx_graph, seed=42)
        highlight_nodes, highlight_edges = self._parse_highlights()
        # Màu nền đỉnh: luôn trắng
        node_colors = ["white" for _ in nx_graph.nodes()]
        # Viền đỉnh: đỉnh highlight có viền đen đậm, đỉnh thường viền xám nhạt
        default_edge_color = "#95a5a6"
        node_edgecolors = []
        node_linewidths = []
        for node in nx_graph.nodes():
            if node in highlight_nodes:
                node_edgecolors.append("black")
                node_linewidths.append(3.0)
            else:
                node_edgecolors.append(default_edge_color)
                node_linewidths.append(2.0)
        # Cạnh highlight: màu đen đậm, dày hơn; cạnh thường xám nhạt, mỏng hơn
        edge_colors = []
        edge_widths = []
        for u, v in nx_graph.edges():
            is_highlighted = (u, v) in highlight_edges or (
                not self.graph.directed and (v, u) in highlight_edges
            )
            if is_highlighted:
                edge_colors.append("black")
                edge_widths.append(2.5)
            else:
                edge_colors.append(default_edge_color)
                edge_widths.append(1.5)
        # Vẽ cạnh trước
        if self.graph.directed:
            # Đồ thị có hướng - sử dụng FancyArrowPatches với margin
            nx.draw_networkx_edges(
                nx_graph,
                self.pos,
                ax=self.ax,
                edge_color=edge_colors,
                arrows=True,
                width=edge_widths,
                arrowsize=20,
                arrowstyle='->',
                min_source_margin=15,
                min_target_margin=15,
                node_size=700,
            )
        else:
            # Đồ thị vô hướng - sử dụng LineCollection đơn giản
            nx.draw_networkx_edges(
                nx_graph,
                self.pos,
                ax=self.ax,
                edge_color=edge_colors,
                width=edge_widths,
            )
        # Vẽ đỉnh với border màu đen nhạt
        nx.draw_networkx_nodes(
            nx_graph,
            self.pos,
            ax=self.ax,
            node_color=node_colors,
            node_size=700,
            edgecolors=node_edgecolors,
            linewidths=node_linewidths,
        )
        # Vẽ label đỉnh
        nx.draw_networkx_labels(
            nx_graph,
            self.pos,
            ax=self.ax,
            font_size=10,
        )
        # Vẽ trọng số phía trên cạnh (nếu có)
        if self.graph.weighted:
            import numpy as np
            labels = nx.get_edge_attributes(nx_graph, "weight")
            for (u, v), weight in labels.items():
                # Lấy tọa độ của hai đỉnh
                x1, y1 = self.pos[u]
                x2, y2 = self.pos[v]
                # Tính điểm giữa cạnh
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                # Tính góc của cạnh để xác định hướng offset
                dx = x2 - x1
                dy = y2 - y1
                # Tránh chia cho 0
                length = np.sqrt(dx**2 + dy**2)
                if length < 0.001:
                    length = 0.001
                # Tính vector vuông góc đơn vị
                # Vector vuông góc (quay 90 độ ngược chiều kim đồng hồ)
                perp_x = -dy / length
                perp_y = dx / length
                # Offset cố định trong không gian màn hình (points)
                # 9 points ≈ 0.3cm trên màn hình chuẩn
                offset_points = 9
                # Vẽ label với offset points (khoảng cách cố định trên màn hình)
                self.ax.annotate(
                    f"{weight:g}",
                    xy=(mid_x, mid_y),  # Vị trí gốc (điểm giữa cạnh)
                    xytext=(perp_x * offset_points, perp_y * offset_points),  # Offset theo hướng vuông góc
                    textcoords='offset points',  # Sử dụng offset points thay vì data coordinates
                    fontsize=9,
                    ha='center', 
                    va='center',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none", alpha=0.8)
                )
        self.ax.axis("off")
        self.canvas.draw_idle()
    # ------------------------------------------------------------------
    # Mouse event handlers cho kéo thả đỉnh và highlight
    # ------------------------------------------------------------------
    def _find_clicked_edge(self, click_x, click_y, threshold=0.1):
        """Tìm cạnh gần nhất với điểm click, trả về (cạnh, khoảng cách)."""
        import numpy as np
        nx_graph = self.graph.to_networkx()
        min_dist = float('inf')
        clicked_edge = None
        for u, v in nx_graph.edges():
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            # Tính khoảng cách từ điểm click đến đường thẳng (u, v)
            dx = x2 - x1
            dy = y2 - y1
            length_sq = dx*dx + dy*dy
            if length_sq < 0.00001:  # Điểm trùng nhau
                continue
            # Tham số t cho điểm chiếu trên đoạn thẳng
            t = max(0, min(1, ((click_x - x1) * dx + (click_y - y1) * dy) / length_sq))
            # Điểm chiếu gần nhất
            proj_x = x1 + t * dx
            proj_y = y1 + t * dy
            # Khoảng cách từ click đến điểm chiếu
            dist = np.sqrt((click_x - proj_x)**2 + (click_y - proj_y)**2)
            if dist < threshold and dist < min_dist:
                min_dist = dist
                clicked_edge = (u, v)
        return clicked_edge, min_dist
    def _on_mouse_press(self, event):
        """Xử lý khi nhấn chuột - phân biệt single click (drag) và double click (highlight)"""
        if event.inaxes != self.ax or self.pos is None or event.xdata is None or event.ydata is None:
            return
        click_pos = (event.xdata, event.ydata)
        # Kiểm tra click vào node - dùng threshold vừa phải để tránh click ngoài vẫn nhận
        node_threshold = 0.15
        clicked_node = None
        min_node_dist = float('inf')
        for node, (x, y) in self.pos.items():
            dist = ((x - click_pos[0])**2 + (y - click_pos[1])**2)**0.5
            if dist < min_node_dist and dist < node_threshold:
                min_node_dist = dist
                clicked_node = node
        # Double-click: ưu tiên đỉnh, chỉ xét cạnh nếu không trúng đỉnh nào
        if event.dblclick:
            # Nếu click nằm trong vùng của một đỉnh -> chỉ toggle đỉnh đó
            if clicked_node is not None:
                if clicked_node in self.highlighted_nodes:
                    self.highlighted_nodes.remove(clicked_node)
                else:
                    self.highlighted_nodes.add(clicked_node)
                self._sync_highlight_inputs()
                self._draw_graph()
                return
            # Không trúng đỉnh nào, thử bắt cạnh gần nhất
            clicked_edge, edge_dist = self._find_clicked_edge(click_pos[0], click_pos[1], threshold=0.1)
            if clicked_edge is not None:
                if clicked_edge in self.highlighted_edges:
                    self.highlighted_edges.remove(clicked_edge)
                else:
                    self.highlighted_edges.add(clicked_edge)
                self._sync_highlight_inputs()
                self._draw_graph()
                return
            # Double-click nhưng không trúng cạnh hay đỉnh -> không làm gì
            return
        # Single click: chỉ dùng cho kéo thả đỉnh
        if clicked_node is not None:
            self.dragging = True
            self.selected_node = clicked_node
            # Lưu offset để kéo mượt hơn, tránh node "nhảy" về vị trí chuột
            node_x, node_y = self.pos[clicked_node]
            self.drag_offset = (node_x - event.xdata, node_y - event.ydata)
            self.canvas.get_tk_widget().config(cursor="hand2")
    def _on_mouse_release(self, event):
        """Xử lý khi thả chuột"""
        self.dragging = False
        self.selected_node = None
        self.drag_offset = None
        self.canvas.get_tk_widget().config(cursor="")
    def _on_mouse_motion(self, event):
        """Xử lý khi di chuyển chuột - chỉ drag khi đang dragging"""
        if not self.dragging or self.selected_node is None or event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return
        # Cập nhật vị trí đỉnh theo offset để di chuyển mượt hơn
        if self.drag_offset is not None:
            dx, dy = self.drag_offset
            new_x = event.xdata + dx
            new_y = event.ydata + dy
        else:
            new_x, new_y = event.xdata, event.ydata
        self.pos[self.selected_node] = (new_x, new_y)
        # Vẽ lại đồ thị
        try:
            self._draw_graph()
        except Exception as e:
            # Nếu có lỗi, in ra để debug nhưng không crash
            print(f"Lỗi khi vẽ: {e}")
def main() -> None:
    app = GraphApp()
    app.mainloop()
if __name__ == "__main__":
    main()


