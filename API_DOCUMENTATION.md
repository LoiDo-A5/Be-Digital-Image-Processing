# Image Processing API Documentation

## Base URL
```
http://localhost:8000/api/image-processing/
```

## Authentication
Hiện tại các API không yêu cầu authentication. Tất cả endpoints đều public.

## Content-Type
Tất cả requests phải sử dụng `multipart/form-data` để upload file ảnh.

## Response Format
Tất cả responses đều trả về JSON format với cấu trúc:
```json
{
    "success": true/false,
    "message": "Thông báo kết quả",
    "processed_image": "data:image/jpeg;base64,...", // Base64 encoded image
    // ... other fields
}
```

---

## 1. Grayscale Conversion API

### Endpoint
```
POST /api/image-processing/grayscale/
```

### Description
Chuyển đổi ảnh màu sang ảnh đen trắng (grayscale).

### Request Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | File | Yes | File ảnh cần xử lý (JPEG, PNG, BMP, TIFF) |

### Request Example (JavaScript)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/api/image-processing/grayscale/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Display processed image
        document.getElementById('result').src = data.processed_image;
    }
});
```

### Response Example
```json
{
    "success": true,
    "message": "Image converted to grayscale successfully",
    "processed_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

### cURL Example
```bash
curl -X POST \
  http://localhost:8000/api/image-processing/grayscale/ \
  -F 'image=@/path/to/image.jpg'
```

---

## 2. Negative Image API

### Endpoint
```
POST /api/image-processing/negative/
```

### Description
Chuyển đổi ảnh sang ảnh âm bản (negative/invert colors).

### Request Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | File | Yes | File ảnh cần xử lý |

### Request Example (JavaScript)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/api/image-processing/negative/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Response Example
```json
{
    "success": true,
    "message": "Image converted to negative successfully",
    "processed_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

---

## 3. Brightness & Contrast Adjustment API

### Endpoint
```
POST /api/image-processing/brightness-contrast/
```

### Description
Điều chỉnh độ sáng và độ tương phản của ảnh.

### Request Parameters
| Parameter | Type | Required | Default | Range | Description |
|-----------|------|----------|---------|-------|-------------|
| `image` | File | Yes | - | - | File ảnh cần xử lý |
| `brightness` | Float | No | 0 | -100 to 100 | Độ sáng (-100: tối nhất, 100: sáng nhất) |
| `contrast` | Float | No | 1.0 | 0.1 to 3.0 | Độ tương phản (0.1: thấp nhất, 3.0: cao nhất) |

### Request Example (JavaScript)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('brightness', '20');    // Tăng độ sáng 20%
formData.append('contrast', '1.5');     // Tăng độ tương phản 50%

fetch('/api/image-processing/brightness-contrast/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Response Example
```json
{
    "success": true,
    "message": "Brightness and contrast adjusted successfully",
    "processed_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "settings": {
        "brightness": 20,
        "contrast": 1.5
    }
}
```

---

## 4. HSV Color Space Conversion API

### Endpoint
```
POST /api/image-processing/hsv-channels/
```

### Description
Chuyển đổi ảnh sang không gian màu HSV và trả về các kênh riêng biệt.

### Request Parameters
| Parameter | Type | Required | Default | Options | Description |
|-----------|------|----------|---------|---------|-------------|
| `image` | File | Yes | - | - | File ảnh cần xử lý |
| `channel` | String | No | 'all' | 'H', 'S', 'V', 'all' | Kênh HSV cần trả về |

### Request Example (JavaScript)
```javascript
// Lấy tất cả kênh HSV
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('channel', 'all');

fetch('/api/image-processing/hsv-channels/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Display all channels
        document.getElementById('h-channel').src = data.H_channel;
        document.getElementById('s-channel').src = data.S_channel;
        document.getElementById('v-channel').src = data.V_channel;
        document.getElementById('hsv-combined').src = data.hsv_channel;
    }
});

// Lấy chỉ kênh H (Hue)
const formData2 = new FormData();
formData2.append('image', fileInput.files[0]);
formData2.append('channel', 'H');

fetch('/api/image-processing/hsv-channels/', {
    method: 'POST',
    body: formData2
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        document.getElementById('result').src = data.processed_image;
    }
});
```

### Response Example (channel='all')
```json
{
    "success": true,
    "message": "HSV conversion completed successfully",
    "H_channel": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "S_channel": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "V_channel": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "hsv_channel": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

### Response Example (channel='H')
```json
{
    "success": true,
    "message": "HSV conversion completed successfully",
    "processed_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "channel": "H"
}
```

---

## 5. Histogram Equalization API

### Endpoint
```
POST /api/image-processing/histogram-equalization/
```

### Description
Áp dụng cân bằng histogram để tăng cường độ tương phản và chất lượng ảnh.

### Request Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | File | Yes | File ảnh cần xử lý |

### Request Example (JavaScript)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('/api/image-processing/histogram-equalization/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Response Example
```json
{
    "success": true,
    "message": "Histogram equalization applied successfully",
    "processed_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
}
```

---

## 6. Multiple Effects API

### Endpoint
```
POST /api/image-processing/multiple-effects/
```

### Description
Áp dụng nhiều hiệu ứng cùng lúc lên một ảnh theo thứ tự được chỉ định.

### Request Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | File | Yes | - | File ảnh cần xử lý |
| `effects` | Array[String] | No | [] | Danh sách hiệu ứng cần áp dụng |
| `brightness` | Float | No | 0 | Độ sáng (chỉ áp dụng khi có 'brightness' trong effects) |
| `contrast` | Float | No | 1.0 | Độ tương phản (chỉ áp dụng khi có 'contrast' trong effects) |

### Available Effects
- `'grayscale'`: Chuyển sang đen trắng
- `'negative'`: Ảnh âm bản
- `'brightness'`: Điều chỉnh độ sáng
- `'contrast'`: Điều chỉnh độ tương phản
- `'histogram_eq'`: Cân bằng histogram

### Request Example (JavaScript)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

// Áp dụng nhiều hiệu ứng: grayscale -> tăng sáng -> cân bằng histogram
const effects = ['grayscale', 'brightness', 'histogram_eq'];
formData.append('effects', JSON.stringify(effects));
formData.append('brightness', '30');

fetch('/api/image-processing/multiple-effects/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Response Example
```json
{
    "success": true,
    "message": "Multiple effects applied successfully",
    "processed_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "applied_effects": ["grayscale", "brightness", "histogram_eq"],
    "settings": {
        "brightness": 30,
        "contrast": 1.0
    }
}
```

---

## 7. Download Processed Image API

### Endpoint
```
POST /api/image-processing/download/
```

### Description
Xử lý ảnh và trả về file để download trực tiếp thay vì base64.

### Request Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | File | Yes | - | File ảnh cần xử lý |
| `effects` | Array[String] | No | [] | Danh sách hiệu ứng cần áp dụng |
| `brightness` | Float | No | 0 | Độ sáng |
| `contrast` | Float | No | 1.0 | Độ tương phản |

### Request Example (JavaScript)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('effects', JSON.stringify(['grayscale', 'brightness']));
formData.append('brightness', '20');

fetch('/api/image-processing/download/', {
    method: 'POST',
    body: formData
})
.then(response => response.blob())
.then(blob => {
    // Tạo link download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'processed_image.jpg';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
});
```

### Response
Trả về file JPEG binary data với headers:
- `Content-Type: image/jpeg`
- `Content-Disposition: attachment; filename="processed_image.jpg"`

---

## 8. Color Analysis API

### Endpoint
```
POST /api/image-processing/color-analysis/
```

### Description
API phân tích và phân biệt màu ảnh với nhiều chế độ hoạt động khác nhau.

### Request Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `image` | File | Yes | - | File ảnh cần phân tích |
| `mode` | String | Yes | - | Chế độ phân tích: `dominant_colors`, `color_detection`, `color_quantization`, `color_mask`, `multi_segment` |

#### Mode-specific Parameters

**For `dominant_colors` mode:**
| Parameter | Type | Required | Default | Range | Description |
|-----------|------|----------|---------|-------|-------------|
| `num_colors` | Integer | No | 5 | 2-20 | Số lượng màu chủ đạo cần trích xuất |

**For `color_detection` mode:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `target_color` | String | Yes | - | Màu mục tiêu (hex format, e.g., #FF0000) |
| `tolerance` | Integer | No | 30 | Độ dung sai màu (1-100) |

**For `color_quantization` mode:**
| Parameter | Type | Required | Default | Range | Description |
|-----------|------|----------|---------|-------|-------------|
| `quantization_levels` | Integer | No | 8 | 2-32 | Số lượng màu trong ảnh sau khi giảm màu |

**For `color_mask` mode:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `color_space` | String | No | 'HSV' | Không gian màu: 'HSV' hoặc 'RGB' |
| `lower_range` | Array[Integer] | Yes | - | Ngưỡng dưới [h/r, s/g, v/b] |
| `upper_range` | Array[Integer] | Yes | - | Ngưỡng trên [h/r, s/g, v/b] |

**For `multi_segment` mode:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `num_segments` | Integer | No | 5 | Số vùng phân đoạn (2-15) |
| `segmentation_method` | String | No | 'kmeans' | Phương pháp: 'kmeans' hoặc 'watershed' |

### Request Examples

#### 1. Dominant Colors Analysis
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('mode', 'dominant_colors');
formData.append('num_colors', '5');

fetch('/api/image-processing/color-analysis/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        console.log('Dominant colors:', data.dominant_colors);
        // Display color palette
        data.dominant_colors.forEach(color => {
            console.log(`Color: ${color.color_hex}, Percentage: ${color.percentage}%`);
        });
    }
});
```

#### 2. Color Detection
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('mode', 'color_detection');
formData.append('target_color', '#FF0000'); // Red color
formData.append('tolerance', '40');

fetch('/api/image-processing/color-analysis/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Display mask
        document.getElementById('mask-result').src = data.mask;
        
        // Show bounding boxes
        console.log('Found regions:', data.bounding_boxes);
    }
});
```

#### 3. Color Quantization
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('mode', 'color_quantization');
formData.append('quantization_levels', '8');

fetch('/api/image-processing/color-analysis/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Display quantized image
        document.getElementById('quantized-result').src = data.quantized_image;
        
        // Show color palette
        console.log('Color palette:', data.color_palette);
    }
});
```

#### 4. Color Mask (HSV)
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('mode', 'color_mask');
formData.append('color_space', 'HSV');
formData.append('lower_range', JSON.stringify([0, 50, 50]));    // Red lower bound
formData.append('upper_range', JSON.stringify([10, 255, 255])); // Red upper bound

fetch('/api/image-processing/color-analysis/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Display mask
        document.getElementById('mask-result').src = data.mask;
        console.log(`Coverage: ${data.coverage_percentage}%`);
    }
});
```

#### 5. Multi-Segment
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);
formData.append('mode', 'multi_segment');
formData.append('num_segments', '6');
formData.append('segmentation_method', 'kmeans');

fetch('/api/image-processing/color-analysis/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // Display each segment
        data.segments.forEach((segment, index) => {
            const img = document.createElement('img');
            img.src = segment.mask;
            img.title = `Segment ${segment.segment_id} - ${segment.coverage_percentage}%`;
            document.getElementById('segments-container').appendChild(img);
        });
    }
});
```

### Response Examples

#### Dominant Colors Response
```json
{
    "success": true,
    "mode": "dominant_colors",
    "message": "Extracted 5 dominant colors successfully",
    "dominant_colors": [
        {
            "color_rgb": [255, 0, 0],
            "color_hex": "#ff0000",
            "percentage": 35.2
        },
        {
            "color_rgb": [0, 255, 0],
            "color_hex": "#00ff00",
            "percentage": 28.7
        }
    ],
    "total_colors": 5
}
```

#### Color Detection Response
```json
{
    "success": true,
    "mode": "color_detection",
    "message": "Detected 3 regions with target color",
    "target_color": "#FF0000",
    "target_color_rgb": [255, 0, 0],
    "tolerance": 30,
    "mask": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "bounding_boxes": [
        {
            "x": 100,
            "y": 150,
            "width": 50,
            "height": 75,
            "area": 3750
        }
    ],
    "regions_found": 3
}
```

#### Color Quantization Response
```json
{
    "success": true,
    "mode": "color_quantization",
    "message": "Image quantized to 8 colors successfully",
    "quantized_image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "color_palette": [
        {
            "color_rgb": [255, 0, 0],
            "color_hex": "#ff0000"
        },
        {
            "color_rgb": [0, 255, 0],
            "color_hex": "#00ff00"
        }
    ],
    "quantization_levels": 8
}
```

#### Color Mask Response
```json
{
    "success": true,
    "mode": "color_mask",
    "message": "Color mask created successfully in HSV color space",
    "color_space": "HSV",
    "color_range": {
        "lower": [0, 50, 50],
        "upper": [10, 255, 255]
    },
    "mask": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
    "coverage_percentage": 15.3,
    "masked_pixels": 12450,
    "total_pixels": 81000
}
```

#### Multi-Segment Response
```json
{
    "success": true,
    "mode": "multi_segment",
    "message": "Image segmented into 5 regions using kmeans",
    "segmentation_method": "kmeans",
    "num_segments": 5,
    "segments": [
        {
            "segment_id": 1,
            "mask": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ...",
            "coverage_percentage": 25.4,
            "pixel_count": 20574,
            "center_color_rgb": [255, 128, 64],
            "center_color_hex": "#ff8040"
        }
    ]
}
```

### cURL Examples

#### Dominant Colors
```bash
curl -X POST \
  http://localhost:8000/api/image-processing/color-analysis/ \
  -F 'image=@/path/to/image.jpg' \
  -F 'mode=dominant_colors' \
  -F 'num_colors=5'
```

#### Color Detection
```bash
curl -X POST \
  http://localhost:8000/api/image-processing/color-analysis/ \
  -F 'image=@/path/to/image.jpg' \
  -F 'mode=color_detection' \
  -F 'target_color=#FF0000' \
  -F 'tolerance=30'
```

#### Color Mask
```bash
curl -X POST \
  http://localhost:8000/api/image-processing/color-analysis/ \
  -F 'image=@/path/to/image.jpg' \
  -F 'mode=color_mask' \
  -F 'color_space=HSV' \
  -F 'lower_range=[0,50,50]' \
  -F 'upper_range=[10,255,255]'
```

### Use Cases

1. **Dominant Colors**: Tạo color palette, phân tích xu hướng màu sắc
2. **Color Detection**: Tìm kiếm object theo màu, quality control
3. **Color Quantization**: Giảm dung lượng ảnh, tạo hiệu ứng poster
4. **Color Mask**: Tách nền, chỉnh sửa selective color
5. **Multi-Segment**: Phân tích cấu trúc ảnh, object segmentation

---

## Error Handling

### Error Response Format
```json
{
    "success": false,
    "message": "Error description"
}
```

### Common Error Cases
1. **File too large (>10MB)**
```json
{
    "success": false,
    "message": "Image size should not exceed 10MB"
}
```

2. **Unsupported file format**
```json
{
    "success": false,
    "message": "Unsupported image format. Allowed formats: JPEG, JPG, PNG, BMP, TIFF"
}
```

3. **Invalid parameters**
```json
{
    "success": false,
    "message": "Invalid effect 'invalid_effect'. Allowed effects: grayscale, negative, brightness, contrast, histogram_eq"
}
```

4. **Server error**
```json
{
    "success": false,
    "message": "Error processing image: [detailed error message]"
}
```

---

## Frontend Integration Examples

### React Component Example
```jsx
import React, { useState } from 'react';

const ImageProcessor = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const processImage = async (endpoint, additionalData = {}) => {
        if (!selectedFile) return;

        setLoading(true);
        const formData = new FormData();
        formData.append('image', selectedFile);
        
        // Add additional parameters
        Object.keys(additionalData).forEach(key => {
            formData.append(key, additionalData[key]);
        });

        try {
            const response = await fetch(`/api/image-processing/${endpoint}/`, {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                setProcessedImage(data.processed_image);
            } else {
                alert(data.message);
            }
        } catch (error) {
            alert('Error processing image');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <input type="file" onChange={handleFileChange} accept="image/*" />
            
            <div>
                <button onClick={() => processImage('grayscale')} disabled={loading}>
                    Grayscale
                </button>
                <button onClick={() => processImage('negative')} disabled={loading}>
                    Negative
                </button>
                <button onClick={() => processImage('brightness-contrast', {
                    brightness: 20,
                    contrast: 1.5
                })} disabled={loading}>
                    Adjust Brightness/Contrast
                </button>
                <button onClick={() => processImage('histogram-equalization')} disabled={loading}>
                    Histogram Equalization
                </button>
            </div>

            {processedImage && (
                <img src={processedImage} alt="Processed" style={{maxWidth: '500px'}} />
            )}
        </div>
    );
};

export default ImageProcessor;
```

### Vue.js Component Example
```vue
<template>
  <div>
    <input type="file" @change="handleFileChange" accept="image/*" />
    
    <div>
      <button @click="processImage('grayscale')" :disabled="loading">
        Grayscale
      </button>
      <button @click="processImage('negative')" :disabled="loading">
        Negative
      </button>
      <button @click="adjustBrightnessContrast" :disabled="loading">
        Adjust Brightness/Contrast
      </button>
    </div>

    <img v-if="processedImage" :src="processedImage" alt="Processed" style="max-width: 500px" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      processedImage: null,
      loading: false
    };
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
    
    async processImage(endpoint, additionalData = {}) {
      if (!this.selectedFile) return;

      this.loading = true;
      const formData = new FormData();
      formData.append('image', this.selectedFile);
      
      Object.keys(additionalData).forEach(key => {
        formData.append(key, additionalData[key]);
      });

      try {
        const response = await fetch(`/api/image-processing/${endpoint}/`, {
          method: 'POST',
          body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
          this.processedImage = data.processed_image;
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert('Error processing image');
      } finally {
        this.loading = false;
      }
    },
    
    adjustBrightnessContrast() {
      this.processImage('brightness-contrast', {
        brightness: 20,
        contrast: 1.5
      });
    }
  }
};
</script>
```

---

## Testing với Postman

### Import Collection
Bạn có thể tạo Postman collection với các request sau:

1. **Grayscale**
   - Method: POST
   - URL: `{{base_url}}/api/image-processing/grayscale/`
   - Body: form-data với key `image` (file)

2. **Brightness/Contrast**
   - Method: POST
   - URL: `{{base_url}}/api/image-processing/brightness-contrast/`
   - Body: form-data với:
     - `image` (file)
     - `brightness` (text): "20"
     - `contrast` (text): "1.5"

3. **Multiple Effects**
   - Method: POST
   - URL: `{{base_url}}/api/image-processing/multiple-effects/`
   - Body: form-data với:
     - `image` (file)
     - `effects` (text): `["grayscale", "brightness"]`
     - `brightness` (text): "30"

### Environment Variables
```
base_url: http://localhost:8000
```
