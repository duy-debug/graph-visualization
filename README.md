# Ứng dụng Quản lý Đồ thị (Graph Manager)
Ứng dụng desktop mô phỏng và trực quan hóa đồ thị, xây dựng bằng **Python + Tkinter + NetworkX + Matplotlib**.

## 📊 Tính năng chính

- ✅ Nhập đồ thị từ bàn phím (ô văn bản) với auto-update
- ✅ Nhập/xuất đồ thị qua file `.txt` theo định dạng chuẩn
- ✅ Tự động phát hiện đồ thị có trọng số hay không từ dữ liệu
- ✅ Tùy chọn đồ thị có hướng/vô hướng
- ✅ Hiển thị ma trận kề và danh sách kề theo thời gian thực
- ✅ Vẽ đồ thị trực quan bằng NetworkX + Matplotlib
- ✅ Kéo thả đỉnh trực tiếp trên canvas để điều chỉnh bố cục
- ✅ Highlight đỉnh/cạnh bằng double-click hoặc nhập text
- ✅ Thêm/xóa đỉnh và cạnh trực tiếp từ giao diện
- ✅ Tính và hiển thị mật độ đồ thị (thưa/dày)
- ✅ Tải dữ liệu mẫu Karate Club (34 đỉnh) để demo

## 🚀 Cài đặt

### 1. Chuẩn bị môi trường

```bash
python -m venv .venv
```

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
source .venv/bin/activate
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## 🎮 Chạy ứng dụng

Từ thư mục gốc project:

```bash
python -m graph_app.app
```

hoặc chạy trực tiếp:

```bash
python graph_app/app.py
```

## 📖 Hướng dẫn sử dụng

### 1. Nhập đồ thị thủ công

- **Ô "Số lượng đỉnh"**: có thể để trống, ứng dụng sẽ tự cập nhật theo danh sách cạnh.
- **Ô "Danh sách cạnh"**: mỗi dòng là **một đỉnh hoặc một cạnh**:
  - Đỉnh đơn lẻ: `A`
  - Cạnh không trọng số: `A B`
  - Cạnh có trọng số: `A B w` (với `w` là số, ví dụ `1`, `2.5`)
- Hỗ trợ tên đỉnh là số (`1`, `2`, `3`) hoặc chữ/chuỗi (`A`, `B`, `C`, ...).

#### Auto-update và tự phát hiện trọng số

- Khi bạn gõ vào ô **Danh sách cạnh**, đồ thị sẽ **tự động cập nhật**:
  - Tự tạo danh sách đỉnh từ các cạnh/đỉnh bạn nhập.
  - Tự cập nhật lại số lượng đỉnh.
  - Nếu có dòng ở dạng `u v w` với `w` là số, ứng dụng sẽ **tự bật chế độ có trọng số**.
- Checkbox **"Đồ thị có trọng số"** sẽ tự thay đổi theo dữ liệu (nhưng bạn vẫn có thể chỉnh thủ công khi cần).

#### Tùy chọn đồ thị

- ☑️ **Đồ thị có hướng**: cạnh `(u, v)` khác với `(v, u)`.
- ☑️ **Đồ thị có trọng số**: cạnh có giá trị trọng số; nếu tắt, mọi cạnh được hiểu là trọng số 1.

### 2. Định dạng file nhập `.txt`

Khi dùng nút **"Đọc file"**, ứng dụng đọc theo **định dạng mới**:

```text
<số_đỉnh>
<cờ_có_hướng>
u1 v1 [w1]
u2 v2 [w2]
...
```

- **Dòng 1**: số đỉnh (số nguyên, ví dụ: `4`).
- **Dòng 2**: cờ có hướng
  - `0` → đồ thị vô hướng
  - `1` → đồ thị có hướng
- **Các dòng tiếp theo**: cạnh
  - `u v` hoặc `u v w`
  - `w` là trọng số (số thực). Nếu có ít nhất một dòng có trọng số hợp lệ, đồ thị sẽ được hiểu là **có trọng số**.

Ví dụ:

```text
4
0
A B 1
A C 1
B D 2
C D 3
```

### 3. Xuất đồ thị ra file

- Dùng nút **"Xuất file"** để lưu cấu trúc đồ thị hiện tại ra `.txt`.
- File xuất ra sẽ bao gồm:
  - Thông tin tổng quan: số đỉnh, có hướng/không, có trọng số hay không.
  - Danh sách cạnh.
  - Ma trận kề.
  - Danh sách kề.

### 4. Thao tác CRUD trên đỉnh/cạnh

- **Thêm đỉnh**: nhập tên đỉnh → bấm **"Thêm đỉnh"**.
- **Xóa đỉnh**: nhập tên đỉnh → bấm **"Xóa đỉnh"**.
- **Thêm cạnh**:
  - Nhập `u`, `v` và (tuỳ chọn) `w` nếu đồ thị có trọng số.
  - Bấm **"Thêm cạnh"**.
  - Ứng dụng sẽ kiểm tra cạnh trùng (với đồ thị không trọng số) và validate trọng số.
- **Xóa cạnh**: nhập `u`, `v` → bấm **"Xóa cạnh"**.

### 5. Highlight và tương tác trực quan

#### Bằng ô nhập text

- **Highlight đỉnh**: nhập danh sách tên đỉnh, cách nhau bởi `,` hoặc `;` (ví dụ: `A,B,C`).
- **Highlight cạnh**: nhập các cạnh dạng `u-v`, `u v` hoặc cách nhau bằng `;`, `,` (ví dụ: `A-B;C-D`).

#### Bằng thao tác chuột trên đồ thị

- **Double-click vào một đỉnh**: bật/tắt highlight đỉnh đó.
- **Double-click gần một cạnh**: bật/tắt highlight cạnh đó.
- **Kéo thả đỉnh**:
  - Single-click giữ chuột lên đỉnh và kéo để thay đổi vị trí.
  - Bố cục sẽ được cập nhật ngay trên canvas.

### 6. Mật độ đồ thị

- Ứng dụng hiển thị **mật độ** ở góc khu vực highlight:
  - Giá trị số từ 0 đến 1.
  - Nhãn: "Đồ thị thưa" hoặc "Đồ thị dày" tùy theo ngưỡng mặc định.

### 7. Dữ liệu mẫu Karate Club

- Nút **"Tải Karate Club"** sẽ tải đồ thị mẫu 34 đỉnh từ thư viện NetworkX.
- Thích hợp để demo nhanh tính năng vẽ, ma trận kề, danh sách kề, mật độ...

### 8. Reset

- Nút **"Reset"** đưa toàn bộ ứng dụng về trạng thái ban đầu:
  - Bỏ tick các checkbox.
  - Xóa toàn bộ dữ liệu nhập, highlight.
  - Xóa thông báo lỗi và vẽ lại đồ thị rỗng.

## 📁 Cấu trúc project

```text
project/
├── .gitignore               # Git ignore file
├── requirements.txt         # Python dependencies
├── README.md                # Tài liệu hướng dẫn (file này)
└── graph_app/               # Python package chính
    ├── __init__.py          # Khởi tạo package
    ├── app.py               # Ứng dụng GUI chính (Tkinter)
    ├── graph_data.py        # Lớp GraphData: lưu trữ + phân tích đồ thị
    └── graph_io.py          # Hàm đọc/ghi đồ thị, Karate Club
```

## 🛠️ Công nghệ sử dụng

- **Python 3.13+**
- **Tkinter** - GUI framework
- **NetworkX** - Thuật toán và mô hình đồ thị
- **Matplotlib** - Vẽ và trực quan hóa đồ thị
