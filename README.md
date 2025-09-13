# HUTECH Telegram Bot

Bot Telegram đa chức năng giúp sinh viên HUTECH truy cập thông tin học tập dễ dàng.

## ✨ Tính năng

-   `/start`: Bắt đầu và xem danh sách lệnh.
-   `/dangnhap`: Đăng nhập vào tài khoản sinh viên.
-   `/dangxuat`: Đăng xuất.
-   `/tkb`: Xem thời khóa biểu và xuất file iCalendar (.ics).
-   `/lichthi`: Xem lịch thi sắp tới.
-   `/diem`: Xem điểm và xuất file Excel.
-   `/hocphan`: Tra cứu thông tin học phần, danh sách sinh viên, lịch sử điểm danh.
-   `/diemdanh`: Điểm danh bằng mã QR hoặc nhập tay.
-   `/trogiup`: Hiển thị trợ giúp.
-   `/huy`: Hủy bỏ thao tác hiện tại.

## 🚀 Cài đặt và Chạy

**Yêu cầu:** Python 3.10+, Git, Docker (khuyến khích).

1.  **Clone repo:**
    ```bash
    git clone https://github.com/vantaidinh04/e-hutech.git
    cd e-hutech
    ```
2.  **Cấu hình:** Sao chép `.env.example` thành `.env` và điền `TELEGRAM_BOT_TOKEN` của bạn.
3.  **Chạy với Docker (Khuyến khích):**
    ```bash
    docker-compose up --build -d
    ```
4.  **Chạy cục bộ:**
    ```bash
    pip install -r requirements.txt
    python bot.py
    ```

## 🛠️ Công nghệ sử dụng

-   [Python](https://www.python.org/)
-   [Postges](https://www.postgresql.org/)
-   [Redis](https://redis.io/)
-   [Docker](https://www.docker.com/)

## 📝 Giấy phép

Dự án này được cấp phép theo Giấy phép Công cộng GNU phiên bản 3. Xem chi tiết tại tệp [LICENSE](LICENSE).
