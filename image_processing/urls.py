from django.urls import path
from .views import (
    GrayscaleImageView,
    NegativeImageView,
    BrightnessContrastView,
    HSVChannelView,
    HistogramEqualizationView,
    MultipleEffectsView,
    ImageDownloadView,
    ColorAnalysisView
)

app_name = 'image_processing'

urlpatterns = [
    # Single effect APIs
    path('grayscale/', GrayscaleImageView.as_view(), name='grayscale'),
    path('negative/', NegativeImageView.as_view(), name='negative'),
    path('brightness-contrast/', BrightnessContrastView.as_view(), name='brightness_contrast'),
    path('hsv-channels/', HSVChannelView.as_view(), name='hsv_channels'),
    path('histogram-equalization/', HistogramEqualizationView.as_view(), name='histogram_equalization'),
    
    # Multiple effects API
    path('multiple-effects/', MultipleEffectsView.as_view(), name='multiple_effects'),
    
    # Color analysis API
    path('color-analysis/', ColorAnalysisView.as_view(), name='color_analysis'),
    
    # Download processed image
    path('download/', ImageDownloadView.as_view(), name='download'),
]
