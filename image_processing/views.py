from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from PIL import Image
import io
import logging

from .serializers import (
    ImageUploadSerializer, 
    ImageProcessingSerializer, 
    BrightnessContrastSerializer,
    HSVChannelSerializer,
    ColorAnalysisSerializer
)
from .utils import (
    pil_to_cv2, 
    cv2_to_pil, 
    image_to_base64,
    apply_grayscale,
    apply_negative,
    adjust_brightness_contrast,
    convert_to_hsv_channels,
    apply_histogram_equalization,
    apply_multiple_effects,
    get_dominant_colors,
    detect_color_regions,
    quantize_colors,
    create_color_mask,
    segment_image_by_color,
    hex_to_rgb,
    gmm_quantize_colors,
    assign_color_names
)

logger = logging.getLogger(__name__)


class GrayscaleImageView(APIView):
    """API để chuyển ảnh sang grayscale (đen trắng)"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = ImageUploadSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                # Apply grayscale
                gray_image = apply_grayscale(cv2_image)
                
                # Convert back to PIL
                result_pil = cv2_to_pil(gray_image)
                
                # Convert to base64
                base64_image = image_to_base64(result_pil)
                
                return Response({
                    'success': True,
                    'message': 'Image converted to grayscale successfully',
                    'processed_image': base64_image
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in grayscale conversion: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NegativeImageView(APIView):
    """API để chuyển ảnh sang ảnh âm bản (negative)"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = ImageUploadSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                # Apply negative effect
                negative_image = apply_negative(cv2_image)
                
                # Convert back to PIL
                result_pil = cv2_to_pil(negative_image)
                
                # Convert to base64
                base64_image = image_to_base64(result_pil)
                
                return Response({
                    'success': True,
                    'message': 'Image converted to negative successfully',
                    'processed_image': base64_image
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in negative conversion: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BrightnessContrastView(APIView):
    """API để điều chỉnh độ sáng và độ tương phản"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = BrightnessContrastSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                brightness = serializer.validated_data['brightness']
                contrast = serializer.validated_data['contrast']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                # Adjust brightness and contrast
                adjusted_image = adjust_brightness_contrast(cv2_image, brightness, contrast)
                
                # Convert back to PIL
                result_pil = cv2_to_pil(adjusted_image)
                
                # Convert to base64
                base64_image = image_to_base64(result_pil)
                
                return Response({
                    'success': True,
                    'message': 'Brightness and contrast adjusted successfully',
                    'processed_image': base64_image,
                    'settings': {
                        'brightness': brightness,
                        'contrast': contrast
                    }
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in brightness/contrast adjustment: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HSVChannelView(APIView):
    """API để chuyển đổi ảnh sang không gian màu HSV và trả về từng kênh"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = HSVChannelSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                channel = serializer.validated_data['channel']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                # Convert to HSV channels
                hsv_channels = convert_to_hsv_channels(cv2_image)
                
                response_data = {
                    'success': True,
                    'message': 'HSV conversion completed successfully'
                }
                
                if channel == 'all':
                    # Return all channels
                    for ch_name, ch_image in hsv_channels.items():
                        result_pil = cv2_to_pil(ch_image)
                        base64_image = image_to_base64(result_pil)
                        response_data[f'{ch_name}_channel'] = base64_image
                else:
                    # Return specific channel
                    if channel in hsv_channels:
                        result_pil = cv2_to_pil(hsv_channels[channel])
                        base64_image = image_to_base64(result_pil)
                        response_data['processed_image'] = base64_image
                        response_data['channel'] = channel
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in HSV conversion: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistogramEqualizationView(APIView):
    """API để áp dụng cân bằng histogram"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = ImageUploadSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                # Apply histogram equalization
                equalized_image = apply_histogram_equalization(cv2_image)
                
                # Convert back to PIL
                result_pil = cv2_to_pil(equalized_image)
                
                # Convert to base64
                base64_image = image_to_base64(result_pil)
                
                return Response({
                    'success': True,
                    'message': 'Histogram equalization applied successfully',
                    'processed_image': base64_image
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in histogram equalization: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MultipleEffectsView(APIView):
    """API để áp dụng nhiều hiệu ứng cùng lúc"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = ImageProcessingSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                effects = serializer.validated_data['effects']
                brightness = serializer.validated_data['brightness']
                contrast = serializer.validated_data['contrast']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                # Apply multiple effects
                processed_image = apply_multiple_effects(
                    cv2_image, effects, brightness, contrast
                )
                
                # Convert back to PIL
                result_pil = cv2_to_pil(processed_image)
                
                # Convert to base64
                base64_image = image_to_base64(result_pil)
                
                return Response({
                    'success': True,
                    'message': 'Multiple effects applied successfully',
                    'processed_image': base64_image,
                    'applied_effects': effects,
                    'settings': {
                        'brightness': brightness,
                        'contrast': contrast
                    }
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in multiple effects processing: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ImageDownloadView(APIView):
    """API để download ảnh đã xử lý"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = ImageProcessingSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                effects = serializer.validated_data['effects']
                brightness = serializer.validated_data['brightness']
                contrast = serializer.validated_data['contrast']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                # Apply effects
                if effects:
                    processed_image = apply_multiple_effects(
                        cv2_image, effects, brightness, contrast
                    )
                else:
                    processed_image = cv2_image
                
                # Convert back to PIL
                result_pil = cv2_to_pil(processed_image)
                
                # Create response for file download
                response = HttpResponse(content_type='image/jpeg')
                response['Content-Disposition'] = 'attachment; filename="processed_image.jpg"'
                
                # Save image to response
                buffer = io.BytesIO()
                result_pil.save(buffer, format='JPEG')
                response.write(buffer.getvalue())
                
                return response
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in image download: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ColorAnalysisView(APIView):
    """API để phân tích và phân biệt màu ảnh với nhiều chế độ hoạt động"""
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            serializer = ColorAnalysisSerializer(data=request.data)
            if serializer.is_valid():
                image_file = serializer.validated_data['image']
                mode = serializer.validated_data['mode']
                
                # Convert to PIL Image
                pil_image = Image.open(image_file)
                
                # Convert to OpenCV format
                cv2_image = pil_to_cv2(pil_image)
                
                response_data = {
                    'success': True,
                    'mode': mode
                }
                
                if mode == 'dominant_colors':
                    num_colors = serializer.validated_data['num_colors']
                    dominant_colors = get_dominant_colors(cv2_image, k=num_colors)
                    
                    response_data.update({
                        'message': f'Extracted {len(dominant_colors)} dominant colors successfully',
                        'dominant_colors': dominant_colors,
                        'total_colors': len(dominant_colors)
                    })
                
                elif mode == 'color_detection':
                    target_color_hex = serializer.validated_data['target_color']
                    tolerance = serializer.validated_data['tolerance']
                    
                    # Convert hex to RGB
                    target_color_rgb = hex_to_rgb(target_color_hex)
                    
                    # Detect color regions
                    mask, bounding_boxes = detect_color_regions(cv2_image, target_color_rgb, tolerance)
                    
                    # Convert mask to base64
                    mask_pil = Image.fromarray(mask)
                    mask_base64 = image_to_base64(mask_pil)
                    
                    response_data.update({
                        'message': f'Detected {len(bounding_boxes)} regions with target color',
                        'target_color': target_color_hex,
                        'target_color_rgb': target_color_rgb,
                        'tolerance': tolerance,
                        'mask': mask_base64,
                        'bounding_boxes': bounding_boxes,
                        'regions_found': len(bounding_boxes)
                    })
                
                elif mode == 'color_quantization':
                    quantization_levels = serializer.validated_data['quantization_levels']
                    
                    # Quantize colors
                    quantized_image, palette = quantize_colors(cv2_image, k=quantization_levels)
                    
                    # Convert to base64
                    result_pil = cv2_to_pil(quantized_image)
                    quantized_base64 = image_to_base64(result_pil)
                    
                    response_data.update({
                        'message': f'Image quantized to {len(palette)} colors successfully',
                        'quantized_image': quantized_base64,
                        'color_palette': palette,
                        'quantization_levels': quantization_levels
                    })
                
                elif mode == 'color_mask':
                    color_space = serializer.validated_data['color_space']
                    lower_range = serializer.validated_data['lower_range']
                    upper_range = serializer.validated_data['upper_range']
                    
                    # Create color range
                    color_range = {
                        'lower': lower_range,
                        'upper': upper_range
                    }
                    
                    # Create mask
                    mask = create_color_mask(cv2_image, color_range, color_space)
                    
                    # Convert mask to base64
                    mask_pil = Image.fromarray(mask)
                    mask_base64 = image_to_base64(mask_pil)
                    
                    # Calculate mask statistics
                    total_pixels = mask.shape[0] * mask.shape[1]
                    white_pixels = cv2.countNonZero(mask)
                    coverage_percentage = (white_pixels / total_pixels) * 100
                    
                    response_data.update({
                        'message': f'Color mask created successfully in {color_space} color space',
                        'color_space': color_space,
                        'color_range': color_range,
                        'mask': mask_base64,
                        'coverage_percentage': round(coverage_percentage, 2),
                        'masked_pixels': int(white_pixels),
                        'total_pixels': int(total_pixels)
                    })
                
                elif mode == 'multi_segment':
                    num_segments = serializer.validated_data['num_segments']
                    segmentation_method = serializer.validated_data['segmentation_method']
                    
                    # Segment image
                    masks, centers = segment_image_by_color(cv2_image, num_segments, segmentation_method)
                    
                    # Convert masks to base64
                    segment_masks = []
                    for i, mask in enumerate(masks):
                        mask_pil = Image.fromarray(mask)
                        mask_base64 = image_to_base64(mask_pil)
                        
                        # Calculate segment statistics
                        total_pixels = mask.shape[0] * mask.shape[1]
                        white_pixels = cv2.countNonZero(mask)
                        coverage_percentage = (white_pixels / total_pixels) * 100
                        
                        segment_info = {
                            'segment_id': i + 1,
                            'mask': mask_base64,
                            'coverage_percentage': round(coverage_percentage, 2),
                            'pixel_count': int(white_pixels)
                        }
                        
                        # Add center color if available (from k-means)
                        if centers is not None and i < len(centers):
                            center_bgr = centers[i]
                            center_rgb = [int(center_bgr[2]), int(center_bgr[1]), int(center_bgr[0])]
                            center_hex = '#{:02x}{:02x}{:02x}'.format(center_rgb[0], center_rgb[1], center_rgb[2])
                            segment_info.update({
                                'center_color_rgb': center_rgb,
                                'center_color_hex': center_hex
                            })
                        
                        segment_masks.append(segment_info)
                    
                    response_data.update({
                        'message': f'Image segmented into {len(masks)} regions using {segmentation_method}',
                        'segmentation_method': segmentation_method,
                        'num_segments': len(masks),
                        'segments': segment_masks
                    })

                elif mode == 'gmm_quantization':
                    n_components = serializer.validated_data['n_components']
                    covariance_type = serializer.validated_data['covariance_type']
                    
                    # Apply GMM-based quantization
                    quant_bgr, palette = gmm_quantize_colors(cv2_image, n_components=n_components, covariance_type=covariance_type)
                    result_pil = cv2_to_pil(quant_bgr)
                    base64_img = image_to_base64(result_pil)
                    
                    response_data.update({
                        'message': f'GMM quantization to {n_components} components completed',
                        'quantized_image': base64_img,
                        'palette': palette,
                        'n_components': n_components,
                        'covariance_type': covariance_type
                    })

                elif mode == 'color_name_palette':
                    # First, compute dominant colors by k-means (reusing quantize_colors)
                    palette_size = serializer.validated_data['palette_size']
                    _, palette = quantize_colors(cv2_image, k=palette_size)
                    
                    # Assign nearest color names
                    enriched = assign_color_names(palette)
                    
                    response_data.update({
                        'message': 'Color names assigned to palette successfully',
                        'palette': enriched,
                        'palette_size': palette_size
                    })
                
                return Response(response_data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            logger.error(f"Error in color analysis: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error processing image: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
