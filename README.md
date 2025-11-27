# Ứng dụng Quản lý Đồ thị (Graph Manager)

Ứng dụng desktop để quản lý và trực quan hóa đồ thị được xây dựng bằng **Python + Tkinter + NetworkX + Matplotlib**.

## 📊 Tính năng chính

- ✅ Nhập đồ thị từ bàn phím hoặc file `.txt`
- ✅ Tùy chọn đồ thị có hướng/vô hướng, có trọng số/không trọng số
- ✅ Hiển thị ma trận kề và danh sách kề tự động
- ✅ Vẽ đồ thị trực quan với NetworkX + Matplotlib
- ✅ Highlight đỉnh/cạnh với màu sắc tùy chỉnh
- ✅ Thêm/xóa đỉnh và cạnh trực tiếp từ giao diện
- ✅ Phân tích mật độ (đồ thị thưa/dày)
- ✅ Xuất cấu trúc đồ thị ra file text
- ✅ Tải dữ liệu mẫu Karate Club (34 đỉnh)
- ✅ Kiểm tra cạnh trùng lặp
- ✅ Validate trọng số

## 🚀 Cài đặt

### 1. Clone repository (hoặc tải về)
```bash
cd project
```

### 2. Tạo virtual environment
```bash
python -m venv .venv
```

### 3. Kích hoạt virtual environment
**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## 🎮 Chạy ứng dụng

```bash
python -m graph_app.app
```

## 📖 Hướng dẫn sử dụng

### Nhập đồ thị thủ công

1. **Nhập đỉnh và cạnh:**
   - Ô **Danh sách cạnh**: mỗi dòng định dạng `u v` (hoặc `u v w` nếu bật trọng số)
   - Hỗ trợ cả số (`1,2,3`) và chữ (`A,B,C`)
   - Đỉnh đơn lẻ (không có cạnh) chỉ cần ghi tên đỉnh

2. **Chọn loại đồ thị:**
   - ☑️ Đồ thị có hướng
   - ☑️ Đồ thị có trọng số

3. **Nhấn "Cập nhật đồ thị"** để hiển thị

### Định dạng file nhập

```
A,B,C,D
A B 1
A C 1
B D 2
C D 3
```

- Dòng đầu: danh sách đỉnh (cách nhau bởi dấu phẩy)
- Các dòng tiếp: `u v [w]` (trọng số `w` chỉ bắt buộc khi bật chế độ có trọng số)

### Thao tác CRUD

- **Thêm đỉnh:** Nhập tên đỉnh → "Thêm đỉnh"
- **Xóa đỉnh:** Nhập tên đỉnh → "Xóa đỉnh"
- **Thêm cạnh:** Nhập u, v, [w] → "Thêm cạnh"
- **Xóa cạnh:** Nhập u, v → "Xóa cạnh"

### Highlight đỉnh/cạnh

- **Đỉnh:** Nhập `A,B,C` → màu vàng
- **Cạnh:** Nhập `A-B;C-D` → màu đỏ
- Nhấn "Vẽ lại với highlight"

## 📁 Cấu trúc project

```
project/
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── README.md               # Documentation (file này)
└── graph_app/              # Main package
    ├── __init__.py         # Package initialization
    ├── app.py              # Main GUI application
    ├── graph_data.py       # Graph data structure
    └── graph_io.py         # I/O operations
```

## 🛠️ Công nghệ sử dụng

- **Python 3.13+**
- **Tkinter** - GUI framework
- **NetworkX** - Graph algorithms and visualization
- **Matplotlib** - Plotting and visualization

## 📝 License

Educational project - NTU 2025-2026
