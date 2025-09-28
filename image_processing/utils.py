import cv2
import numpy as np
from PIL import Image
import base64
import io


def pil_to_cv2(pil_image):
    """Convert PIL Image to OpenCV format"""
    # Convert PIL image to RGB if it's not already
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    
    # Convert to numpy array and change color order from RGB to BGR
    cv2_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return cv2_image


def cv2_to_pil(cv2_image):
    """Convert OpenCV image to PIL Image"""
    # Convert color order from BGR to RGB
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    # Convert to PIL Image
    pil_image = Image.fromarray(rgb_image)
    return pil_image


def image_to_base64(image, format='JPEG'):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/{format.lower()};base64,{img_str}"


def apply_grayscale(cv2_image):
    """Convert image to grayscale"""
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    # Convert back to 3-channel for consistency
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


def apply_negative(cv2_image):
    """Apply negative effect to image"""
    return 255 - cv2_image


def adjust_brightness_contrast(cv2_image, brightness=0, contrast=1.0):
    """
    Adjust brightness and contrast of image
    brightness: -100 to 100
    contrast: 0.1 to 3.0
    """
    # Convert brightness from -100,100 to -255,255 range
    brightness = int(brightness * 2.55)
    
    # Apply brightness and contrast
    adjusted = cv2.convertScaleAbs(cv2_image, alpha=contrast, beta=brightness)
    return adjusted


def convert_to_hsv_channels(cv2_image):
    """
    Convert image to HSV and return individual channels
    Returns: dict with 'H', 'S', 'V' channels and 'hsv' combined
    """
    hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    # Convert single channels back to 3-channel for display
    h_3ch = cv2.cvtColor(h, cv2.COLOR_GRAY2BGR)
    s_3ch = cv2.cvtColor(s, cv2.COLOR_GRAY2BGR)
    v_3ch = cv2.cvtColor(v, cv2.COLOR_GRAY2BGR)
    hsv_3ch = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    return {
        'H': h_3ch,
        'S': s_3ch,
        'V': v_3ch,
        'hsv': hsv_3ch
    }


def apply_histogram_equalization(cv2_image):
    """Apply histogram equalization to enhance image contrast"""
    # Convert to YUV color space
    yuv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2YUV)
    
    # Apply histogram equalization to the Y channel (luminance)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    
    # Convert back to BGR
    result = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
    return result


def apply_clahe(cv2_image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
    # Convert to LAB color space
    lab = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2LAB)
    
    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    
    # Convert back to BGR
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return result


def apply_multiple_effects(cv2_image, effects, brightness=0, contrast=1.0):
    """
    Apply multiple effects to an image in sequence
    effects: list of effect names
    """
    result = cv2_image.copy()
    
    for effect in effects:
        if effect == 'grayscale':
            result = apply_grayscale(result)
        elif effect == 'negative':
            result = apply_negative(result)
        elif effect == 'brightness':
            result = adjust_brightness_contrast(result, brightness=brightness, contrast=1.0)
        elif effect == 'contrast':
            result = adjust_brightness_contrast(result, brightness=0, contrast=contrast)
        elif effect == 'histogram_eq':
            result = apply_histogram_equalization(result)
        elif effect == 'clahe':
            result = apply_clahe(result)
    
    return result


# Color Analysis Functions
def get_dominant_colors(cv2_image, k=5):
    """
    Extract dominant colors from image using K-means clustering
    Returns: list of colors with percentages
    """
    from sklearn.cluster import KMeans
    
    # Reshape image to be a list of pixels
    data = cv2_image.reshape((-1, 3))
    data = np.float32(data)
    
    # Apply K-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert centers to uint8
    centers = np.uint8(centers)
    
    # Calculate percentages
    unique_labels, counts = np.unique(labels, return_counts=True)
    percentages = (counts / len(labels)) * 100
    
    # Sort by percentage (descending)
    sorted_indices = np.argsort(percentages)[::-1]
    
    dominant_colors = []
    for i in sorted_indices:
        color_bgr = centers[i]
        color_rgb = [int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0])]  # BGR to RGB
        hex_color = '#{:02x}{:02x}{:02x}'.format(color_rgb[0], color_rgb[1], color_rgb[2])
        
        dominant_colors.append({
            'color_rgb': color_rgb,
            'color_hex': hex_color,
            'percentage': float(percentages[i])
        })
    
    return dominant_colors


def detect_color_regions(cv2_image, target_color_rgb, tolerance=30):
    """
    Detect regions similar to target color
    target_color_rgb: [R, G, B] values
    tolerance: color similarity threshold
    Returns: mask and bounding boxes
    """
    # Convert target color to BGR
    target_bgr = np.array([target_color_rgb[2], target_color_rgb[1], target_color_rgb[0]])
    
    # Create mask for similar colors
    lower_bound = np.clip(target_bgr - tolerance, 0, 255)
    upper_bound = np.clip(target_bgr + tolerance, 0, 255)
    
    mask = cv2.inRange(cv2_image, lower_bound, upper_bound)
    
    # Find contours for bounding boxes
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bounding_boxes = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Filter small regions
            x, y, w, h = cv2.boundingRect(contour)
            bounding_boxes.append({
                'x': int(x),
                'y': int(y),
                'width': int(w),
                'height': int(h),
                'area': int(cv2.contourArea(contour))
            })
    
    return mask, bounding_boxes


def quantize_colors(cv2_image, k=8):
    """
    Reduce number of colors using K-means clustering
    Returns: quantized image and color palette
    """
    # Reshape image
    data = cv2_image.reshape((-1, 3))
    data = np.float32(data)
    
    # Apply K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert centers to uint8
    centers = np.uint8(centers)
    
    # Create quantized image
    quantized_data = centers[labels.flatten()]
    quantized_image = quantized_data.reshape(cv2_image.shape)
    
    # Create palette
    palette = []
    for center in centers:
        color_rgb = [int(center[2]), int(center[1]), int(center[0])]  # BGR to RGB
        hex_color = '#{:02x}{:02x}{:02x}'.format(color_rgb[0], color_rgb[1], color_rgb[2])
        palette.append({
            'color_rgb': color_rgb,
            'color_hex': hex_color
        })
    
    return quantized_image, palette


def create_color_mask(cv2_image, color_range, color_space='HSV'):
    """
    Create binary mask based on color range
    color_range: {'lower': [h1, s1, v1], 'upper': [h2, s2, v2]} for HSV
                 or {'lower': [r1, g1, b1], 'upper': [r2, g2, b2]} for RGB
    """
    if color_space.upper() == 'HSV':
        # Convert to HSV
        hsv_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
        lower_bound = np.array(color_range['lower'])
        upper_bound = np.array(color_range['upper'])
        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    else:  # RGB
        # Convert BGR to RGB for processing
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        lower_bound = np.array(color_range['lower'])
        upper_bound = np.array(color_range['upper'])
        mask = cv2.inRange(rgb_image, lower_bound, upper_bound)
    
    return mask


def segment_image_by_color(cv2_image, n_segments=5, method='kmeans'):
    """
    Segment image into N color regions
    method: 'kmeans' or 'watershed'
    Returns: list of masks for each segment
    """
    if method == 'kmeans':
        # Reshape image
        data = cv2_image.reshape((-1, 3))
        data = np.float32(data)
        
        # Apply K-means
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
        _, labels, centers = cv2.kmeans(data, n_segments, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Create masks for each segment
        labels = labels.reshape(cv2_image.shape[:2])
        masks = []
        
        for i in range(n_segments):
            mask = (labels == i).astype(np.uint8) * 255
            masks.append(mask)
        
        return masks, centers
    
    elif method == 'watershed':
        # Convert to grayscale for watershed
        gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # Sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        
        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        
        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        
        # Marker labelling
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        
        # Apply watershed
        markers = cv2.watershed(cv2_image, markers)
        
        # Create masks for each segment
        masks = []
        unique_markers = np.unique(markers)
        
        for marker in unique_markers:
            if marker > 1:  # Skip background (0) and border (-1)
                mask = (markers == marker).astype(np.uint8) * 255
                masks.append(mask)
        
        return masks, None


def hex_to_rgb(hex_color):
    """Convert hex color to RGB"""
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]


def rgb_to_hsv_range(rgb_color, tolerance=10):
    """Convert RGB color to HSV range for masking"""
    # Convert single RGB pixel to HSV
    rgb_pixel = np.uint8([[rgb_color]])
    hsv_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_RGB2HSV)[0][0]
    
    # Create range with tolerance
    lower_hsv = np.clip(hsv_pixel - tolerance, [0, 50, 50], [179, 255, 255])
    upper_hsv = np.clip(hsv_pixel + tolerance, [0, 50, 50], [179, 255, 255])
    
    return {
        'lower': lower_hsv.tolist(),
        'upper': upper_hsv.tolist()
    }


# ================= ML-based color analysis utilities =================
def _sample_pixels_for_model(cv2_image, max_samples=50000, colorspace='BGR'):
    """Randomly sample up to max_samples pixels for model fitting to speed up."""
    img = cv2_image
    h, w = img.shape[:2]
    data = img.reshape(-1, 3)
    n = data.shape[0]
    if n > max_samples:
        idx = np.random.choice(n, size=max_samples, replace=False)
        data = data[idx]
    if colorspace == 'RGB':
        data = data[:, ::-1]
    return np.float32(data)


def gmm_quantize_colors(cv2_image, n_components=8, covariance_type='tied'):
    """
    Reduce colors using Gaussian Mixture Model.
    Returns: quantized_image (BGR), palette (list of dict with rgb, hex, weight).
    """
    from sklearn.mixture import GaussianMixture

    # Fit GMM on sampled RGB pixels for better color representation
    samples_rgb = _sample_pixels_for_model(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB), colorspace='RGB')
    gmm = GaussianMixture(n_components=n_components, covariance_type=covariance_type, random_state=42)
    gmm.fit(samples_rgb)

    # Use means as palette centers in RGB
    centers_rgb = np.clip(gmm.means_, 0, 255).astype(np.uint8)
    weights = gmm.weights_

    # Assign each pixel to nearest component (predict)
    h, w = cv2_image.shape[:2]
    pixels_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB).reshape(-1, 3)
    labels = gmm.predict(np.float32(pixels_rgb))
    quantized_rgb = centers_rgb[labels].reshape(h, w, 3)
    quantized_bgr = cv2.cvtColor(quantized_rgb, cv2.COLOR_RGB2BGR)

    # Build palette with weights
    palette = []
    for i, center in enumerate(centers_rgb):
        color_rgb = [int(center[0]), int(center[1]), int(center[2])]
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color_rgb)
        palette.append({
            'color_rgb': color_rgb,
            'color_hex': hex_color,
            'weight': float(weights[i] * 100.0)
        })

    # Sort palette by weight desc
    palette.sort(key=lambda x: x['weight'], reverse=True)
    return quantized_bgr, palette


# Color name mapping (CSS3 basic color set)
_CSS3_COLORS = [
    ("black", [0, 0, 0]), ("white", [255, 255, 255]), ("red", [255, 0, 0]),
    ("lime", [0, 255, 0]), ("blue", [0, 0, 255]), ("yellow", [255, 255, 0]),
    ("cyan", [0, 255, 255]), ("magenta", [255, 0, 255]), ("silver", [192, 192, 192]),
    ("gray", [128, 128, 128]), ("maroon", [128, 0, 0]), ("olive", [128, 128, 0]),
    ("green", [0, 128, 0]), ("purple", [128, 0, 128]), ("teal", [0, 128, 128]),
    ("navy", [0, 0, 128]), ("orange", [255, 165, 0]), ("pink", [255, 192, 203]),
    ("brown", [165, 42, 42]), ("gold", [255, 215, 0])
]


def _rgb_to_lab(rgb):
    # rgb list to Lab using OpenCV
    rgb_pixel = np.uint8([[rgb]])  # shape (1,1,3)
    lab_pixel = cv2.cvtColor(rgb_pixel, cv2.COLOR_RGB2LAB)[0][0]
    return lab_pixel.astype(np.float32)


def _delta_e_lab(lab1, lab2):
    # Simple Euclidean in Lab space
    return float(np.linalg.norm(lab1 - lab2))


def nearest_color_name(rgb):
    """Find nearest CSS3 color name for a given rgb list using Lab distance."""
    lab = _rgb_to_lab(rgb)
    best = (None, 1e9)
    for name, ref_rgb in _CSS3_COLORS:
        d = _delta_e_lab(lab, _rgb_to_lab(ref_rgb))
        if d < best[1]:
            best = (name, d)
    return {'name': best[0], 'distance': best[1]}


def assign_color_names(palette):
    """
    Given a palette list [{'color_rgb': [r,g,b], 'color_hex': '#xxxxxx', ...}],
    append nearest color names.
    """
    enriched = []
    for item in palette:
        info = nearest_color_name(item['color_rgb'])
        new_item = dict(item)
        new_item['nearest_name'] = info['name']
        new_item['name_distance'] = info['distance']
        enriched.append(new_item)
    return enriched
