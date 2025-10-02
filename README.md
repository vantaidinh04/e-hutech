# HUTECH Telegram Bot

Bot Telegram đa chức năng được thiết kế dành riêng cho sinh viên HUTECH, giúp truy cập thông tin học tập một cách nhanh chóng và thuận tiện ngay trên nền tảng Telegram.

## ✨ Tính năng nổi bật

| Lệnh | Chức năng |
| :--- | :--- |
| `/start` | Bắt đầu tương tác và hiển thị danh sách các lệnh có sẵn. |
| `/dangnhap` | Đăng nhập vào tài khoản sinh viên cá nhân. |
| `/dangxuat` | Đăng xuất khỏi tài khoản. |
| `/tkb` | Xem thời khóa biểu tuần hiện tại và xuất tệp iCalendar (.ics). |
| `/lichthi` | Xem lịch thi các môn sắp tới. |
| `/diem` | Xem điểm số và xuất ra tệp Excel. |
| `/hocphan` | Tra cứu thông tin chi tiết về học phần, danh sách lớp, và lịch sử điểm danh. |
| `/diemdanh` | Thực hiện điểm danh nhanh chóng bằng mã. |
| `/trogiup` | Hiển thị thông tin trợ giúp chi tiết. |
| `/huy` | Hủy bỏ thao tác đang thực hiện. |

## 🚀 Hướng dẫn Cài đặt và Chạy

### Yêu cầu tiên quyết

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/products/docker-desktop/) (Khuyến khích cho việc triển khai)

### Cài đặt chung

1.  **Clone repository về máy của bạn:**
    ```bash
    git clone https://github.com/vantaidinh04/e-hutech.git
    cd e-hutech
    ```

2.  **Cấu hình môi trường:**
    Sao chép tệp cấu hình mẫu và điền thông tin cần thiết.
    ```bash
    cp .env.example .env
    ```
    Sau đó, mở tệp `.env` và điền `TELEGRAM_BOT_TOKEN` của bạn.

### Lựa chọn 1: Chạy với Docker (Khuyến khích)

Đây là phương pháp được khuyến khích để đảm bảo tính nhất quán và dễ dàng triển khai.

1.  **Build và chạy container:**
    ```bash
    docker-compose up --build -d
    ```
    Lệnh này sẽ:
    - Tạo và khởi động các container cho PostgreSQL, Redis và bot
    - Tự động kiểm tra sức khỏe của các dịch vụ
    - Bot sẽ chỉ khởi động sau khi PostgreSQL và Redis sẵn sàng

2.  **Kiểm tra logs (tùy chọn):**
    ```bash
    docker-compose logs -f hutech-bot  # Chỉ xem logs của bot
    docker-compose logs -f            # Xem logs của tất cả services
    ```

3.  **Kiểm tra trạng thái các container:**
    ```bash
    docker-compose ps
    ```

4.  **Dừng bot:**
    ```bash
    docker-compose down    # Dừng và xóa containers
    docker-compose down -v # Dừng và xóa containers kèm volumes
    ```

5.  **Khởi động lại sau khi thay
    ```bash
    docker-compose up --build -d --force-recreate
    ```

### Lựa chọn 2: Chạy ở môi trường cục bộ

Phương pháp này phù hợp cho việc phát triển và gỡ lỗi.

**Lưu ý:** Bạn cần cài đặt và chạy PostgreSQL và Redis trên máy local trước khi chạy bot.

1.  **Tạo và kích hoạt môi trường ảo:**
    -   **Trên macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   **Trên Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

2.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Khởi chạy bot:**
    ```bash
    python bot.py
    ```

4.  **Ngắt kích hoạt môi trường ảo khi hoàn tất:**
    ```bash
    deactivate
    ```

## 📝 Giấy phép

Dự án này được cấp phép theo Giấy phép Công cộng GNU phiên bản 3. Xem chi tiết tại tệp [LICENSE](LICENSE).
