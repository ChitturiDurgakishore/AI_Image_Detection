from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .gemini_service import analyze_image
import json
from PIL import Image, ImageDraw
import io
import base64


def add_analysis_overlay(image_file, result):
    """Add visual indicators to the image based on analysis results."""
    try:
        image_file.seek(0)
        img = Image.open(image_file)
        
        # Create a copy to draw on
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy, 'RGBA')
        
        width, height = img_copy.size
        
        # If AI-generated, add subtle highlighting to draw attention
        if result['answer'] == 'AI':
            # Add a subtle border glow to indicate AI detection
            border_color = (255, 152, 0, 80)  # Orange with transparency
            border_width = 3
            for i in range(border_width):
                draw.rectangle(
                    [(i, i), (width - i - 1, height - i - 1)],
                    outline=border_color,
                    width=1
                )
            
            # Add some indicator circles if suspicious regions are mentioned
            if 'suspicious_regions' in result and result['suspicious_regions'] and 'none' not in result['suspicious_regions'].lower():
                suspicious_lower = result['suspicious_regions'].lower()
                circle_radius = max(20, min(width, height) * 0.1)
                # map keywords to a relative location on the image
                mapping = {
                    'eye': (0.3, 0.2),
                    'eyes': (0.3, 0.2),
                    'face': (0.5, 0.3),
                    'hand': (0.7, 0.6),
                    'hands': (0.7, 0.6),
                    'background': (0.5, 0.5),
                    'sky': (0.5, 0.15),
                    'text': (0.5, 0.8),
                    'edge': (0.9, 0.5),
                    'texture': (0.4, 0.6),
                    'mouth': (0.5, 0.35)
                }
                drawn = 0
                for key, (rx, ry) in mapping.items():
                    if key in suspicious_lower and drawn < 5:
                        x = width * rx
                        y = height * ry
                        draw.ellipse([
                            (x - circle_radius, y - circle_radius),
                            (x + circle_radius, y + circle_radius)
                        ], outline=(255, 152, 0, 200), width=3)
                        drawn += 1
                # if nothing matched, fallback to central circle
                if drawn == 0:
                    x = width * 0.5
                    y = height * 0.5
                    draw.ellipse([
                        (x - circle_radius, y - circle_radius),
                        (x + circle_radius, y + circle_radius)
                    ], outline=(255, 152, 0, 200), width=3)
        else:
            # For real images, add a subtle green border
            border_color = (40, 167, 69, 50)  # Green with transparency
            border_width = 2
            for i in range(border_width):
                draw.rectangle(
                    [(i, i), (width - i - 1, height - i - 1)],
                    outline=border_color,
                    width=1
                )
        
        # Convert back to base64
        img_byte_arr = io.BytesIO()
        img_copy.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        image_data = img_byte_arr.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        return f"data:image/png;base64,{base64_image}"
    except Exception as e:
        # If overlay fails, return original
        image_file.seek(0)
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/png;base64,{base64_image}"


def index(request):
    """Render the image detection form."""
    if request.method == 'POST':
        if 'image' not in request.FILES:
            return render(request, 'detector/index.html', {
                'error': 'No image file provided.'
            })
        
        image_file = request.FILES['image']
        
        try:
            result = analyze_image(image_file)
            
            # Always get the original image for display
            image_file.seek(0)
            original_data = image_file.read()
            original_src = f"data:image/jpeg;base64,{base64.b64encode(original_data).decode('utf-8')}"
            
            # Always generate the circled overlay version
            circled_src = add_analysis_overlay(image_file, result)
            
            # Get Gemini's annotated image if available
            annotated = result.get('annotated_image')
            
            return render(request, 'detector/index.html', {
                'result': result['answer'],
                'confidence': result.get('confidence', 'Medium'),
                'analysis': result.get('analysis', ''),
                'suspicious_regions': result.get('suspicious_regions', ''),
                'full_response': result.get('full_response', ''),
                'original_src': original_src,
                'circled_src': circled_src,
                'annotated_src': annotated
            })
        except Exception as e:
            return render(request, 'detector/index.html', {
                'error': str(e)
            })
    
    return render(request, 'detector/index.html')
