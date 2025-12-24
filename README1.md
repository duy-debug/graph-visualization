# ỨNG DỤNG QUẢN LÝ VÀ TRỰC QUAN HÓA ĐỒ THỊ

**Sinh viên thực hiện:** Trần Mai Ngọc Duy - MSSV: 65130650  
**Lớp:** 65CNTT1  
**Giảng viên hướng dẫn:** ThS. Phạm Thị Thu Thúy  
**Đề tài:** Đồ án cơ sở ngành - MÔ PHỎNG BIỂU DIỄN ĐỒ THỊ BẰNG MA TRẬN KỀ & DANH SÁCH KỀ 

---

## MÔ TẢ DỰ ÁN

Ứng dụng **Graph Manager** là một công cụ desktop chuyên nghiệp được phát triển bằng ngôn ngữ Python, cho phép người dùng mô hình hóa, quản lý và trực quan hóa các cấu trúc đồ thị phức tạp. Ứng dụng hỗ trợ đa dạng các loại đồ thị và cung cấp các công cụ phân tích dữ liệu trực quan theo thời gian thực.

### Mục tiêu chính
- Trực quan hóa cấu trúc đồ thị một cách sinh động và dễ hiểu.
- Cung cấp công cụ quản lý dữ liệu đồ thị (thêm, xóa, sửa đỉnh/cạnh) linh hoạt.
- Phân tích và trình bày dữ liệu dưới dạng Ma trận kề và Danh sách kề.
- Hỗ trợ nhập liệu thông minh từ tệp tin và tương tác chuột trực tiếp.

---

## TÍNH NĂNG CHÍNH

### 1. Quản lý Dữ liệu Thông minh
- **Nhập liệu linh hoạt**: Nhập danh sách cạnh trực tiếp với tính năng tự động cập nhật (Auto-update).
- **Xử lý tệp tin (.txt)**: Đọc và ghi dữ liệu đồ thị theo định dạng chuẩn, hỗ trợ xuất báo cáo chi tiết.
- **Tự động nhận diện**: Hệ thống tự động phát hiện các thuộc tính đồ thị (có hướng, có trọng số) dựa trên dữ liệu đầu vào.

### 2. Trực quan hóa & Tương tác
- **Đồ họa sống động**: Sử dụng NetworkX và Matplotlib để tính toán bố cục (Layout) và vẽ đồ thị chuyên nghiệp.
- **Tương tác kéo thả**: Người dùng có thể dùng chuột để di chuyển đỉnh trên không gian vẽ (Canvas).
- **Hệ thống Highlight**: Đánh dấu nổi bật các đỉnh và cạnh quan trọng qua thao tác double-click hoặc nhập liệu văn bản.

### 3. Phân tích & Trình bày
- **Ma trận kề & Danh sách kề**: Hiển thị song song hai dạng biểu diễn đồ thị phổ biến nhất.
- **Chỉ số mật độ**: Tính toán và phân loại đồ thị (thưa/dày) theo các metrics toán học.
- **Dữ liệu mẫu**: Tích hợp đồ thị mẫu nổi tiếng (Zachary's Karate Club) để thử nghiệm tính năng.

---

## CÔNG NGHỆ SỬ DỤNG

| Công nghệ | Vai trò |
|-----------|-----------|
| **Python 3.13+** | Ngôn ngữ phát triển cốt lõi |
| **Tkinter** | Xây dựng giao diện ứng dụng desktop |
| **NetworkX** | Xử lý logic đồ thị và các thuật toán bố cục |
| **Matplotlib** | Trực quan hóa đồ họa và tương tác trên Canvas |

---

## CẤU TRÚC MÃ NGUỒN

- **`graph_app/app.py`**: Trái tim của ứng dụng, quản lý giao diện chính, điều khiển sự kiện và đồng bộ dữ liệu.
- **`graph_app/graph_data.py`**: Thành phần Model, định nghĩa cấu trúc dữ liệu Graph và các phép toán cơ bản.
- **`graph_app/graph_io.py`**: Tiện ích I/O, xử lý việc nạp file, xuất báo cáo và dữ liệu mẫu.

---

## HƯỚNG DẪN CÀI ĐẶT & CHẠY

1. **Cài đặt thư viện**: 
   ```bash
   pip install -r requirements.txt
   ```
2. **Chạy ứng dụng**:
   ```bash
   python -m graph_app.app
   ```

---

## TÀI LIỆU VÀ BẢN QUYỀN

Dự án này được phát triển trong khuôn khổ môn **Đồ án cơ sở ngành** tại **Trường Đại học Nha Trang**.

**Sinh viên:** Trần Mai Ngọc Duy  
**MSSV:** 65130650  
**Thời gian hoàn thành:** Tháng 12/2025
