# Image Processing API Documentation

## Tổng quan
API xử lý ảnh cung cấp các tính năng xử lý màu hình ảnh cho đồ án môn Xử lý ảnh.

## Cài đặt Dependencies
```bash
poetry install
# hoặc
pip install opencv-python numpy pillow
```

## Các API Endpoints

### 1. Chuyển ảnh sang Grayscale (Đen trắng)
**Endpoint:** `POST /api/image-processing/grayscale/`

**Parameters:**
- `image` (file): File ảnh cần xử lý

**Response:**
```json
{
    "success": true,
    "message": "Image converted to grayscale successfully",
    "processed_image": "data:image/jpeg;base64,..."
}
```

**Curl Example:**
```bash
curl -X POST \
  http://localhost:8000/api/image-processing/grayscale/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@path/to/your/image.jpg'
```

### 2. Chuyển ảnh sang Negative (Âm bản)
**Endpoint:** `POST /api/image-processing/negative/`

**Parameters:**
- `image` (file): File ảnh cần xử lý

**Response:**
```json
{
    "success": true,
    "message": "Image converted to negative successfully",
    "processed_image": "data:image/jpeg;base64,..."
}
```

### 3. Điều chỉnh Độ sáng và Độ tương phản
**Endpoint:** `POST /api/image-processing/brightness-contrast/`

**Parameters:**
- `image` (file): File ảnh cần xử lý
- `brightness` (float, optional): Độ sáng (-100 đến 100, mặc định: 0)
- `contrast` (float, optional): Độ tương phản (0.1 đến 3.0, mặc định: 1.0)

**Response:**
```json
{
    "success": true,
    "message": "Brightness and contrast adjusted successfully",
    "processed_image": "data:image/jpeg;base64,...",
    "settings": {
        "brightness": 20,
        "contrast": 1.5
    }
}
```

**Curl Example:**
```bash
curl -X POST \
  http://localhost:8000/api/image-processing/brightness-contrast/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@path/to/your/image.jpg' \
  -F 'brightness=20' \
  -F 'contrast=1.5'
```

### 4. Chuyển đổi sang không gian màu HSV
**Endpoint:** `POST /api/image-processing/hsv-channels/`

**Parameters:**
- `image` (file): File ảnh cần xử lý
- `channel` (string, optional): Kênh cần trả về ('H', 'S', 'V', 'all', mặc định: 'all')

**Response (channel='all'):**
```json
{
    "success": true,
    "message": "HSV conversion completed successfully",
    "H_channel": "data:image/jpeg;base64,...",
    "S_channel": "data:image/jpeg;base64,...",
    "V_channel": "data:image/jpeg;base64,...",
    "hsv_channel": "data:image/jpeg;base64,..."
}
```

**Response (channel='H'):**
```json
{
    "success": true,
    "message": "HSV conversion completed successfully",
    "processed_image": "data:image/jpeg;base64,...",
    "channel": "H"
}
```

### 5. Cân bằng Histogram
**Endpoint:** `POST /api/image-processing/histogram-equalization/`

**Parameters:**
- `image` (file): File ảnh cần xử lý

**Response:**
```json
{
    "success": true,
    "message": "Histogram equalization applied successfully",
    "processed_image": "data:image/jpeg;base64,..."
}
```

### 6. Áp dụng nhiều hiệu ứng
**Endpoint:** `POST /api/image-processing/multiple-effects/`

**Parameters:**
- `image` (file): File ảnh cần xử lý
- `effects` (array, optional): Danh sách hiệu ứng ['grayscale', 'negative', 'brightness', 'contrast', 'histogram_eq']
- `brightness` (float, optional): Độ sáng (-100 đến 100, mặc định: 0)
- `contrast` (float, optional): Độ tương phản (0.1 đến 3.0, mặc định: 1.0)

**Response:**
```json
{
    "success": true,
    "message": "Multiple effects applied successfully",
    "processed_image": "data:image/jpeg;base64,...",
    "applied_effects": ["grayscale", "brightness"],
    "settings": {
        "brightness": 20,
        "contrast": 1.0
    }
}
```

**Curl Example:**
```bash
curl -X POST \
  http://localhost:8000/api/image-processing/multiple-effects/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@path/to/your/image.jpg' \
  -F 'effects=["grayscale", "brightness"]' \
  -F 'brightness=30'
```

### 7. Download ảnh đã xử lý
**Endpoint:** `POST /api/image-processing/download/`

**Parameters:**
- `image` (file): File ảnh cần xử lý
- `effects` (array, optional): Danh sách hiệu ứng
- `brightness` (float, optional): Độ sáng
- `contrast` (float, optional): Độ tương phản

**Response:** File ảnh JPEG để download

## Định dạng ảnh được hỗ trợ
- JPEG/JPG
- PNG
- BMP
- TIFF

## Giới hạn
- Kích thước file tối đa: 10MB
- Định dạng response: Base64 hoặc file download

## Ví dụ sử dụng với Python requests

```python
import requests

# Upload và xử lý ảnh
url = "http://localhost:8000/api/image-processing/grayscale/"
files = {'image': open('test_image.jpg', 'rb')}

response = requests.post(url, files=files)
result = response.json()

if result['success']:
    # Lấy ảnh đã xử lý dạng base64
    processed_image = result['processed_image']
    print("Xử lý ảnh thành công!")
else:
    print(f"Lỗi: {result['message']}")
```

## Ví dụ sử dụng với JavaScript/Fetch

```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('brightness', '20');
formData.append('contrast', '1.5');

fetch('/api/image-processing/brightness-contrast/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Hiển thị ảnh đã xử lý
        const img = document.createElement('img');
        img.src = data.processed_image;
        document.body.appendChild(img);
    }
});
```
