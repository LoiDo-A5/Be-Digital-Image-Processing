# Hướng dẫn cài đặt và chạy project Django ở môi trường local sử dụng Docker Compose

## 🚀 Hướng dẫn cài đặt và chạy project ở môi trường local

### ⚙️ Yêu cầu
Trước khi bắt đầu, bạn cần đảm bảo máy đã cài đặt:
- Docker
- Docker Compose

### 🔧 Các bước cài đặt và chạy project

1. **Clone project từ GitHub (nếu cần)**
    ```bash
    git clone https://github.com/your-username/your-repo.git
    cd your-repo
    ```

2. **Build Docker containers**
    ```bash
    docker-compose build
    ```
    Lệnh này sẽ build toàn bộ các container định nghĩa trong file `docker-compose.yml`.

3. **Khởi chạy Docker containers**
    ```bash
    docker-compose up
    ```

4. **Kiểm tra các container đã chạy**
    ```bash
    docker-compose ps
    ```

5. **Apply migrations cho database**
    ```bash
    docker compose exec app poetry run python manage.py migrate
    ```

6. **Tạo superuser để đăng nhập vào Django admin**
    ```bash
    docker compose exec app poetry run python manage.py createsuperuser
    ```

7. **Truy cập ứng dụng**
    Mở trình duyệt và vào địa chỉ:
    ```bash
    http://localhost:8000/admin
    ```
    Đăng nhập bằng tài khoản user admin đã tạo.

8. **(Tuỳ chọn) Truy cập vào Django shell để test**
    ```bash
    docker compose exec app poetry run python manage.py shell
    ```

### 📁 Cấu trúc volume & network

#### Volumes:
- **postgres_data**: Dữ liệu PostgreSQL sẽ được lưu tại đây để không mất khi container bị xoá.

#### Networks:
- **backend**: Các service `app`, `db`, và `redis` nằm chung network này để có thể giao tiếp với nhau.
