from rest_framework import serializers


class ImageUploadSerializer(serializers.Serializer):
    """Serializer for image upload"""
    image = serializers.ImageField(required=True)
    
    def validate_image(self, value):
        """Validate uploaded image"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("Image size should not exceed 10MB")
        
        # Check file format
        allowed_formats = ['JPEG', 'JPG', 'PNG', 'BMP', 'TIFF']
        if hasattr(value, 'image'):
            if value.image.format not in allowed_formats:
                raise serializers.ValidationError(f"Unsupported image format. Allowed formats: {', '.join(allowed_formats)}")
        
        return value


class ImageProcessingSerializer(serializers.Serializer):
    """Serializer for image processing with multiple effects"""
    image = serializers.ImageField(required=True)
    effects = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
        help_text="List of effects to apply: grayscale, negative, brightness, contrast, histogram_eq"
    )
    brightness = serializers.FloatField(required=False, default=0, min_value=-100, max_value=100)
    contrast = serializers.FloatField(required=False, default=1.0, min_value=0.1, max_value=3.0)
    
    def validate_effects(self, value):
        """Validate effects list"""
        allowed_effects = ['grayscale', 'negative', 'brightness', 'contrast', 'histogram_eq']
        for effect in value:
            if effect not in allowed_effects:
                raise serializers.ValidationError(f"Invalid effect '{effect}'. Allowed effects: {', '.join(allowed_effects)}")
        return value


class BrightnessContrastSerializer(serializers.Serializer):
    """Serializer for brightness and contrast adjustment"""
    image = serializers.ImageField(required=True)
    brightness = serializers.FloatField(default=0, min_value=-100, max_value=100, help_text="Brightness adjustment (-100 to 100)")
    contrast = serializers.FloatField(default=1.0, min_value=0.1, max_value=3.0, help_text="Contrast multiplier (0.1 to 3.0)")


class HSVChannelSerializer(serializers.Serializer):
    """Serializer for HSV channel extraction"""
    image = serializers.ImageField(required=True)
    channel = serializers.ChoiceField(
        choices=['H', 'S', 'V', 'all'],
        default='all',
        help_text="HSV channel to extract: H (Hue), S (Saturation), V (Value), or all"
    )


class ColorAnalysisSerializer(serializers.Serializer):
    """Serializer for color analysis with multiple modes"""
    image = serializers.ImageField(required=True)
    mode = serializers.ChoiceField(
        choices=['dominant_colors', 'color_detection', 'color_quantization', 'color_mask', 'multi_segment'],
        required=True,
        help_text="Analysis mode: dominant_colors, color_detection, color_quantization, color_mask, multi_segment"
    )
    
    # Parameters for dominant_colors mode
    num_colors = serializers.IntegerField(
        default=5, min_value=2, max_value=20,
        help_text="Number of dominant colors to extract (2-20)"
    )
    
    # Parameters for color_detection mode
    target_color = serializers.CharField(
        required=False, max_length=7,
        help_text="Target color in hex format (e.g., #FF0000 for red)"
    )
    tolerance = serializers.IntegerField(
        default=30, min_value=1, max_value=100,
        help_text="Color similarity tolerance (1-100)"
    )
    
    # Parameters for color_quantization mode
    quantization_levels = serializers.IntegerField(
        default=8, min_value=2, max_value=32,
        help_text="Number of colors in quantized image (2-32)"
    )
    
    # Parameters for color_mask mode
    color_space = serializers.ChoiceField(
        choices=['HSV', 'RGB'],
        default='HSV',
        help_text="Color space for masking: HSV or RGB"
    )
    lower_range = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=255),
        required=False,
        help_text="Lower bound for color range [h/r, s/g, v/b]"
    )
    upper_range = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=255),
        required=False,
        help_text="Upper bound for color range [h/r, s/g, v/b]"
    )
    
    # Parameters for multi_segment mode
    num_segments = serializers.IntegerField(
        default=5, min_value=2, max_value=15,
        help_text="Number of segments for multi-segmentation (2-15)"
    )
    segmentation_method = serializers.ChoiceField(
        choices=['kmeans', 'watershed'],
        default='kmeans',
        help_text="Segmentation method: kmeans or watershed"
    )
    
    def validate(self, data):
        """Custom validation based on mode"""
        mode = data.get('mode')
        
        if mode == 'color_detection':
            if not data.get('target_color'):
                raise serializers.ValidationError("target_color is required for color_detection mode")
            
            # Validate hex color format
            target_color = data.get('target_color')
            if not target_color.startswith('#') or len(target_color) != 7:
                raise serializers.ValidationError("target_color must be in hex format (e.g., #FF0000)")
        
        elif mode == 'color_mask':
            if not data.get('lower_range') or not data.get('upper_range'):
                raise serializers.ValidationError("lower_range and upper_range are required for color_mask mode")
            
            lower_range = data.get('lower_range', [])
            upper_range = data.get('upper_range', [])
            
            if len(lower_range) != 3 or len(upper_range) != 3:
                raise serializers.ValidationError("lower_range and upper_range must contain exactly 3 values")
            
            # Validate HSV ranges
            if data.get('color_space') == 'HSV':
                if not (0 <= lower_range[0] <= 179 and 0 <= upper_range[0] <= 179):
                    raise serializers.ValidationError("HSV Hue values must be between 0-179")
        
        return data
