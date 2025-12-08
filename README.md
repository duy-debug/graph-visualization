# ỨNG DỤNG QUẢN LÝ VÀ TRỰC QUAN HÓA ĐỒ THỊ

**Sinh viên thực hiện:** Trần Mai Ngọc Duy - MSSV: 65130650  
**Lớp:** 65CNTT1  
**Giảng viên hướng dẫn:** ThS. Phạm Thị Thu Thủy  
**Đề tài:** Thực tập cơ sở - Ứng dụng mô phỏng và trực quan hóa đồ thị

---

## 📋 MÔ TẢ DỰ ÁN

Ứng dụng **Graph Manager** là một công cụ desktop được phát triển bằng Python, cho phép người dùng tạo, quản lý, và trực quan hóa các loại đồ thị khác nhau. Ứng dụng hỗ trợ cả đồ thị có hướng/vô hướng, có trọng số/không trọng số, và cung cấp nhiều tính năng tương tác trực quan để phân tích cấu trúc đồ thị.

### Mục tiêu dự án

- Xây dựng giao diện trực quan, dễ sử dụng cho việc làm việc với đồ thị
- Hỗ trợ nhiều cách nhập liệu: thủ công, từ file, hoặc dữ liệu mẫu
- Hiển thị đồ thị dưới nhiều dạng: trực quan (canvas), ma trận kề, danh sách kề
- Cho phép thao tác CRUD (Create, Read, Update, Delete) trên đỉnh và cạnh
- Tính toán và hiển thị các thuộc tính của đồ thị (mật độ, số cạnh, v.v.)
- Hỗ trợ tương tác trực tiếp với đồ thị qua chuột (kéo thả, highlight)

---

## 🎯 TÍNH NĂNG CHÍNH

### 1. Quản lý đồ thị cơ bản

- ✅ **Nhập đồ thị từ bàn phím**: Nhập danh sách cạnh với tính năng auto-update theo thời gian thực
- ✅ **Nhập/xuất file**: Đọc và ghi đồ thị theo định dạng chuẩn `.txt`
- ✅ **Tự động phát hiện thuộc tính**: Tự động nhận diện đồ thị có trọng số từ dữ liệu nhập
- ✅ **Tùy chọn linh hoạt**: Chuyển đổi giữa đồ thị có hướng/vô hướng, có trọng số/không trọng số

### 2. Hiển thị và trực quan hóa

- ✅ **Vẽ đồ thị**: Sử dụng NetworkX và Matplotlib để vẽ đồ thị với bố cục tự động
- ✅ **Ma trận kề**: Hiển thị ma trận kề theo thời gian thực
- ✅ **Danh sách kề**: Hiển thị danh sách kề với định dạng rõ ràng
- ✅ **Tính mật độ**: Tự động tính và phân loại đồ thị (thưa/dày)

### 3. Thao tác CRUD

- ✅ **Thêm/xóa đỉnh**: Thêm hoặc xóa đỉnh với validation đầy đủ
- ✅ **Thêm/xóa cạnh**: Quản lý cạnh với kiểm tra trùng lặp và validation trọng số
- ✅ **Cập nhật trực tiếp**: Mọi thay đổi được phản ánh ngay lập tức trên giao diện

### 4. Tương tác trực quan

- ✅ **Kéo thả đỉnh**: Single-click và kéo để điều chỉnh vị trí đỉnh trên canvas
- ✅ **Highlight đỉnh/cạnh**: 
  - Double-click trực tiếp lên đỉnh/cạnh để highlight
  - Nhập danh sách đỉnh/cạnh cần highlight qua text box
- ✅ **Tương tác chuột**: Phân biệt rõ ràng giữa single-click (drag) và double-click (highlight)

### 5. Tính năng bổ sung

- ✅ **Dữ liệu mẫu Karate Club**: Tải đồ thị mẫu 34 đỉnh để demo và thử nghiệm
- ✅ **Reset toàn bộ**: Đưa ứng dụng về trạng thái ban đầu với một click
- ✅ **Thông báo lỗi**: Hiển thị thông báo lỗi rõ ràng khi có vấn đề với dữ liệu nhập

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

| Công nghệ | Phiên bản | Mục đích sử dụng |
|-----------|-----------|------------------|
| **Python** | 3.13+ | Ngôn ngữ lập trình chính |
| **Tkinter** | Built-in | Framework GUI cho giao diện desktop |
| **NetworkX** | ≥ 3.0 | Thư viện xử lý và phân tích đồ thị |
| **Matplotlib** | ≥ 3.5.0 | Thư viện vẽ và trực quan hóa đồ thị |

---

## 📁 CẤU TRÚC DỰ ÁN

```
Basic_internship_project/
│
├── .git/                                    # Git repository
├── .gitignore                               # Git ignore configuration
├── requirements.txt                         # Python dependencies
├── README.md                                # Tài liệu hướng dẫn (file này)
│
├── BaoCaoTTCS_TranMaiNgocDuy_65130650_65cntt1.docx  # Báo cáo Word
├── DeTai Thuc tap co so_GV.Pham Thi Thu Thuy_65-CNTT.pdf  # Đề tài
│
└── graph_app/                               # Package chính của ứng dụng
    ├── __init__.py                          # Khởi tạo Python package
    ├── app.py                               # Ứng dụng GUI chính (927 dòng)
    ├── graph_data.py                        # Class GraphData - quản lý dữ liệu đồ thị
    ├── graph_io.py                          # Module đọc/ghi file và load dữ liệu mẫu
    │
    ├── test_graph1.txt                      # File test đồ thị có hướng, có trọng số
    ├── test_graph2.txt                      # File test đồ thị có hướng, trọng số hỗn hợp
    ├── test_graph3.txt                      # File test đồ thị vô hướng, có trọng số
    └── result.txt                           # File kết quả xuất mẫu
```

### Chi tiết các module

#### 1. `app.py` - Ứng dụng GUI chính
- **Class `GraphApp(tk.Tk)`**: Lớp chính kế thừa từ Tkinter
- **Chức năng chính**:
  - Xây dựng giao diện người dùng với các widget
  - Xử lý sự kiện người dùng (click, input, drag-drop)
  - Quản lý trạng thái highlight và tương tác chuột
  - Vẽ và cập nhật đồ thị theo thời gian thực
  - Đồng bộ hóa giữa các view khác nhau (canvas, ma trận, danh sách kề)

#### 2. `graph_data.py` - Quản lý dữ liệu đồ thị
- **Class `GraphData`**: Dataclass quản lý cấu trúc đồ thị
- **Thuộc tính**:
  - `directed`: Boolean - đồ thị có hướng hay không
  - `weighted`: Boolean - đồ thị có trọng số hay không
  - `nodes`: List[str] - danh sách các đỉnh
  - `adjacency`: Dict[str, Dict[str, float]] - ma trận kề dạng dictionary
- **Phương thức chính**:
  - `add_node()`, `remove_node()`: Quản lý đỉnh
  - `add_edge()`, `remove_edge()`: Quản lý cạnh
  - `adjacency_matrix()`: Trả về ma trận kề dạng 2D array
  - `adjacency_list()`: Trả về danh sách kề
  - `density()`: Tính mật độ đồ thị
  - `to_networkx()`: Chuyển đổi sang NetworkX Graph object

#### 3. `graph_io.py` - Xử lý I/O
- **Hàm `read_graph_from_text()`**: Parse đồ thị từ chuỗi text
- **Hàm `read_graph_from_file()`**: Đọc đồ thị từ file .txt
- **Hàm `export_graph_to_file()`**: Xuất đồ thị ra file với đầy đủ thông tin
- **Hàm `load_karate_club()`**: Load đồ thị mẫu Karate Club từ NetworkX

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### Yêu cầu hệ thống

- **Hệ điều hành**: Windows 10/11, macOS, hoặc Linux
- **Python**: Phiên bản 3.13 trở lên (khuyến nghị 3.13+)
- **RAM**: Tối thiểu 4GB
- **Dung lượng**: ~100MB cho môi trường ảo và dependencies

### Các bước cài đặt

#### Bước 1: Clone hoặc tải project

```bash
# Nếu sử dụng Git
git clone <repository-url>
cd Basic_internship_project

# Hoặc giải nén file zip đã tải về
```

#### Bước 2: Tạo môi trường ảo (Virtual Environment)

**Trên Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Trên macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Bước 3: Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

Lệnh này sẽ cài đặt:
- `networkx>=3.0` - Thư viện xử lý đồ thị
- `matplotlib>=3.5.0` - Thư viện vẽ đồ thị

#### Bước 4: Kiểm tra cài đặt

```bash
python -c "import networkx; import matplotlib; print('Cài đặt thành công!')"
```

---

## 🎮 HƯỚNG DẪN SỬ DỤNG

### Chạy ứng dụng

Từ thư mục gốc của project, chạy một trong hai lệnh sau:

```bash
# Cách 1: Chạy như một module
python -m graph_app.app

# Cách 2: Chạy trực tiếp file
python graph_app/app.py
```

### 1. Nhập đồ thị thủ công

#### Nhập số lượng đỉnh
- Ô **"Số lượng đỉnh"** có thể để trống
- Ứng dụng sẽ tự động cập nhật số đỉnh dựa trên danh sách cạnh

#### Nhập danh sách cạnh
Trong ô **"Danh sách cạnh"**, mỗi dòng có thể là:

- **Đỉnh đơn lẻ**: `A` (tạo đỉnh không có cạnh)
- **Cạnh không trọng số**: `A B`
- **Cạnh có trọng số**: `A B 5` (với 5 là trọng số)

**Ví dụ:**
```
A
B C
C D 2.5
D A 3
```

#### Tính năng Auto-update
- Khi gõ vào ô "Danh sách cạnh", đồ thị tự động cập nhật:
  - Tự tạo danh sách đỉnh từ các cạnh
  - Tự cập nhật số lượng đỉnh
  - Tự phát hiện và bật checkbox "Đồ thị có trọng số" nếu phát hiện trọng số

#### Tùy chọn đồ thị
- ☑️ **Đồ thị có hướng**: Cạnh (u, v) khác với (v, u)
- ☑️ **Đồ thị có trọng số**: Cạnh có giá trị trọng số; nếu tắt, mọi cạnh = 1

### 2. Nhập đồ thị từ file

#### Định dạng file `.txt`

```
<số_đỉnh>
<cờ_có_hướng>
u1 v1 [w1]
u2 v2 [w2]
...
```

**Chi tiết:**
- **Dòng 1**: Số đỉnh (số nguyên, ví dụ: `4`)
- **Dòng 2**: Cờ có hướng
  - `0` → đồ thị vô hướng
  - `1` → đồ thị có hướng
- **Các dòng tiếp theo**: Danh sách cạnh
  - `u v` (không trọng số)
  - `u v w` (có trọng số)

**Ví dụ file `test_graph3.txt`:**
```
3
0
a b 5
b c 3
c a 2
```

#### Cách sử dụng
1. Click nút **"Đọc file"**
2. Chọn file `.txt` từ hộp thoại
3. Đồ thị sẽ được load tự động với đầy đủ thuộc tính

### 3. Xuất đồ thị ra file

1. Click nút **"Xuất file"**
2. Chọn vị trí và tên file để lưu
3. File xuất ra sẽ bao gồm:
   - Thông tin tổng quan (số đỉnh, có hướng/không, có trọng số/không)
   - Danh sách cạnh
   - Ma trận kề (dạng bảng)
   - Danh sách kề

**Ví dụ file xuất:**
```
Số lượng đỉnh: 2
Đồ thị: vô hướng
Trọng số: không

Danh sách cạnh:
a b

Ma trận kề:
#	a	b
a	0	1
b	1	0

Danh sách kề:
a -> b
b -> a
```

### 4. Thao tác CRUD trên đỉnh và cạnh

#### Thêm đỉnh
1. Nhập tên đỉnh vào ô **"Tên đỉnh"**
2. Click nút **"Thêm đỉnh"**
3. Đỉnh mới sẽ xuất hiện trên đồ thị

#### Xóa đỉnh
1. Nhập tên đỉnh cần xóa
2. Click nút **"Xóa đỉnh"**
3. Đỉnh và tất cả cạnh liên quan sẽ bị xóa

#### Thêm cạnh
1. Nhập đỉnh nguồn `u` và đỉnh đích `v`
2. Nếu đồ thị có trọng số, nhập trọng số `w`
3. Click nút **"Thêm cạnh"**
4. Ứng dụng sẽ kiểm tra:
   - Cạnh có tồn tại chưa (tránh trùng)
   - Trọng số có hợp lệ không

#### Xóa cạnh
1. Nhập đỉnh nguồn `u` và đỉnh đích `v`
2. Click nút **"Xóa cạnh"**

### 5. Highlight và tương tác trực quan

#### Highlight bằng text input

**Highlight đỉnh:**
- Nhập danh sách tên đỉnh, cách nhau bởi `,` hoặc `;`
- Ví dụ: `A,B,C` hoặc `A;B;C`

**Highlight cạnh:**
- Nhập các cạnh dạng `u-v` hoặc `u v`, cách nhau bằng `;` hoặc `,`
- Ví dụ: `A-B;C-D` hoặc `A B,C D`

#### Highlight bằng chuột

**Double-click vào đỉnh:**
- Bật/tắt highlight đỉnh đó
- Đỉnh được highlight sẽ có màu khác biệt

**Double-click gần cạnh:**
- Bật/tắt highlight cạnh đó
- Cạnh được highlight sẽ có màu và độ dày khác

#### Kéo thả đỉnh

**Single-click và kéo:**
1. Click và giữ chuột trên một đỉnh
2. Kéo đỉnh đến vị trí mong muốn
3. Thả chuột để cố định vị trí mới
4. Bố cục đồ thị sẽ cập nhật ngay lập tức

### 6. Xem thông tin đồ thị

#### Ma trận kề
- Hiển thị ở tab **"Ma trận kề"**
- Dạng bảng 2D với header là tên đỉnh
- Giá trị là trọng số (hoặc 0/1 nếu không có trọng số)

#### Danh sách kề
- Hiển thị ở tab **"Danh sách kề"**
- Mỗi dòng: `đỉnh -> danh_sách_đỉnh_kề`
- Nếu có trọng số: `đỉnh -> đỉnh_kề(trọng_số), ...`

#### Mật độ đồ thị
- Hiển thị ở góc phải khu vực highlight
- **Công thức**:
  - Đồ thị có hướng: `density = E / (V × (V-1))`
  - Đồ thị vô hướng: `density = 2E / (V × (V-1))`
- **Phân loại**:
  - Mật độ ≥ 0.5: "Đồ thị dày"
  - Mật độ < 0.5: "Đồ thị thưa"

### 7. Tải dữ liệu mẫu

#### Karate Club Graph
- Click nút **"Tải Karate Club"**
- Load đồ thị mẫu 34 đỉnh từ thư viện NetworkX
- Đồ thị mô tả mạng xã hội trong một câu lạc bộ karate
- Thích hợp để demo và test các tính năng

### 8. Reset ứng dụng

- Click nút **"Reset"** để:
  - Bỏ tick tất cả checkbox
  - Xóa toàn bộ dữ liệu nhập
  - Xóa highlight
  - Xóa thông báo lỗi
  - Vẽ lại đồ thị rỗng

---

## 📊 KIẾN TRÚC VÀ THIẾT KẾ

### Mô hình MVC (Model-View-Controller)

Ứng dụng được thiết kế theo mô hình MVC đơn giản:

- **Model** (`graph_data.py`): Quản lý dữ liệu và logic nghiệp vụ của đồ thị
- **View** (`app.py` - phần GUI): Hiển thị giao diện và đồ thị
- **Controller** (`app.py` - phần xử lý sự kiện): Xử lý tương tác người dùng

### Luồng dữ liệu

```
User Input → Controller → Model (GraphData) → View Update
     ↑                                              ↓
     └──────────────── User Interaction ────────────┘
```

### Các design pattern được sử dụng

1. **Dataclass Pattern**: `GraphData` sử dụng `@dataclass` để giảm boilerplate code
2. **Observer Pattern**: Auto-update khi dữ liệu thay đổi
3. **Factory Pattern**: `to_networkx()` tạo NetworkX graph object
4. **Separation of Concerns**: Tách biệt logic nghiệp vụ, I/O, và GUI

---

## 🧪 TESTING VÀ VALIDATION

### Test cases có sẵn

Project bao gồm 3 file test:

1. **test_graph1.txt**: Đồ thị có hướng, có trọng số, có đỉnh đơn lẻ
2. **test_graph2.txt**: Đồ thị có hướng, trọng số hỗn hợp (một số cạnh có, một số không)
3. **test_graph3.txt**: Đồ thị vô hướng, có trọng số, tạo thành tam giác

### Validation được implement

- ✅ Kiểm tra định dạng file input
- ✅ Kiểm tra trùng lặp cạnh
- ✅ Kiểm tra tồn tại đỉnh khi thêm cạnh
- ✅ Kiểm tra định dạng trọng số (phải là số)
- ✅ Kiểm tra cú pháp highlight input
- ✅ Hiển thị thông báo lỗi rõ ràng cho người dùng

---

## 🔧 TROUBLESHOOTING

### Lỗi thường gặp và cách khắc phục

#### 1. Lỗi: "No module named 'networkx'"
**Nguyên nhân**: Chưa cài đặt dependencies  
**Giải pháp**:
```bash
pip install -r requirements.txt
```

#### 2. Lỗi: "Tkinter not found"
**Nguyên nhân**: Python không có Tkinter (hiếm gặp)  
**Giải pháp**:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Tkinter thường có sẵn
- **Windows**: Tkinter có sẵn trong Python installer

#### 3. Đồ thị không hiển thị
**Nguyên nhân**: Matplotlib backend issue  
**Giải pháp**: Thử chạy lại hoặc cài đặt lại matplotlib:
```bash
pip uninstall matplotlib
pip install matplotlib
```

#### 4. File không đọc được
**Nguyên nhân**: Sai định dạng file  
**Giải pháp**: Kiểm tra file theo đúng định dạng:
```
<số_đỉnh>
<0 hoặc 1>
u v [w]
...
```

---

## 📝 HƯỚNG PHÁT TRIỂN

### Các tính năng có thể mở rộng

1. **Thuật toán đồ thị**:
   - Tìm đường đi ngắn nhất (Dijkstra, Bellman-Ford)
   - Tìm cây khung nhỏ nhất (Kruskal, Prim)
   - Tìm kiếm theo chiều rộng/sâu (BFS/DFS)
   - Phát hiện chu trình

2. **Cải thiện UI/UX**:
   - Dark mode
   - Tùy chỉnh màu sắc đỉnh/cạnh
   - Zoom in/out canvas
   - Undo/Redo

3. **Export/Import**:
   - Hỗ trợ nhiều định dạng file (JSON, CSV, GraphML)
   - Export hình ảnh đồ thị (PNG, SVG)
   - Import từ các nguồn khác (database, API)

4. **Phân tích nâng cao**:
   - Tính toán centrality (degree, betweenness, closeness)
   - Phát hiện community
   - Tính toán các metrics khác (diameter, radius, clustering coefficient)

5. **Performance**:
   - Tối ưu hóa cho đồ thị lớn (>1000 đỉnh)
   - Lazy loading
   - Caching

---

## 📚 TÀI LIỆU THAM KHẢO

1. **NetworkX Documentation**: https://networkx.org/documentation/stable/
2. **Matplotlib Documentation**: https://matplotlib.org/stable/contents.html
3. **Tkinter Documentation**: https://docs.python.org/3/library/tkinter.html
4. **Graph Theory**:
   - "Introduction to Graph Theory" - Douglas B. West
   - "Graph Theory with Applications" - Bondy & Murty

---

## 📄 GIẤY PHÉP VÀ BẢN QUYỀN

Dự án này được phát triển cho mục đích học tập trong khuôn khổ môn Thực tập cơ sở tại Đại học Nha Trang.

**Sinh viên thực hiện:** Trần Mai Ngọc Duy - 65130650  
**Giảng viên hướng dẫn:** ThS. Phạm Thị Thu Thủy  
**Năm học:** 2025-2026, Học kỳ 1

---

## 📞 LIÊN HỆ VÀ HỖ TRỢ

Nếu có bất kỳ thắc mắc hoặc vấn đề nào trong quá trình sử dụng, vui lòng liên hệ:

- **Email sinh viên**: 
- **MSSV**: 65130650
- **Lớp**: 65CNTT1

---

## 🙏 LỜI CẢM ƠN

Em xin chân thành cảm ơn:
- **ThS. Phạm Thị Thu Thủy** - Giảng viên hướng dẫn, đã tận tình chỉ bảo và hỗ trợ em trong suốt quá trình thực hiện đề tài
- **Khoa Công nghệ Thông tin** - Đại học Nha Trang, đã tạo điều kiện thuận lợi cho em học tập và nghiên cứu
- **Các bạn sinh viên lớp 65CNTT1** - Đã đóng góp ý kiến và hỗ trợ trong quá trình phát triển ứng dụng

---

**Ngày hoàn thành:** Tháng 12/2025  
**Phiên bản:** 1.0.0
