"""
Service module to handle Google Gemini Vision API calls for image analysis.
"""
import google.generativeai as genai
from django.conf import settings
import base64
import io


def analyze_image(image_file):
    """
    Analyze an image using Google Gemini Vision API to determine if it's AI-generated or real.
    
    Args:
        image_file: Uploaded image file from Django request.FILES
    
    Returns:
        dict: Contains 'answer' (AI/Real) and 'reason' (explanation)
    
    Raises:
        ValueError: If API key is not configured
        Exception: If API call fails
    """
    api_key = settings.GEMINI_API_KEY
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable not set. "
            "Please set it in your .env file or environment."
        )
    
    # Configure the Gemini API
    genai.configure(api_key=api_key)
    
    # Read image file, resize for faster processing, and encode to base64
    image_file.seek(0)
    from PIL import Image as PILImage
    img = PILImage.open(image_file)
    
    # Convert RGBA to RGB (JPEG doesn't support transparency)
    if img.mode == 'RGBA':
        rgb_img = PILImage.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
        img = rgb_img
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize to max 1024px on longest side to reduce processing time and avoid 504 timeouts
    max_size = 1024
    img.thumbnail((max_size, max_size), PILImage.Resampling.LANCZOS)
    
    # Save resized image to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=85)
    img_byte_arr.seek(0)
    image_data = img_byte_arr.read()
    base64_image = base64.standard_b64encode(image_data).decode('utf-8')
    
    # Determine MIME type from file name
    file_name = image_file.name.lower()
    if file_name.endswith('.png'):
        mime_type = 'image/png'
    elif file_name.endswith('.gif'):
        mime_type = 'image/gif'
    elif file_name.endswith('.webp'):
        mime_type = 'image/webp'
    else:
        mime_type = 'image/jpeg'
    
    # Create the message with the image
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    prompt = """Analyze this image and determine if it's AI-generated or real.

Respond in this exact format:
CLASSIFICATION: AI or Real
CONFIDENCE: High/Medium/Low
ANALYSIS: 2-3 sentences explaining findings
SUSPICIOUS_REGIONS: Specific areas with artifacts or say None detected

Be concise.
"""
    
    message = model.generate_content([
        {
            "role": "user",
            "parts": [
                {
                    "inline_data": {
                        "mime_type": mime_type,
                        "data": base64_image,
                    }
                },
                prompt
            ]
        }
    ])
    
    # Parse the response
    response_text = message.text.strip()
    
    # Extract structured information
    lines = response_text.split('\n')
    classification = 'Unknown'
    confidence = 'Medium'
    analysis = ''
    suspicious_regions = ''
    
    for line in lines:
        line_lower = line.lower()
        if line_lower.startswith('classification:'):
            classification = line.split(':', 1)[1].strip().split()[0]  # Get first word
        elif line_lower.startswith('confidence:'):
            confidence = line.split(':', 1)[1].strip().split()[0]
        elif line_lower.startswith('analysis:'):
            analysis = line.split(':', 1)[1].strip()
        elif line_lower.startswith('suspicious_regions:'):
            suspicious_regions = line.split(':', 1)[1].strip()
    
    # Normalize classification
    if 'AI' in classification.upper():
        answer = 'AI'
    elif 'REAL' in classification.upper():
        answer = 'Real'
    else:
        answer = 'Unknown'
    
    annotated_image = None
    # look for ANNOTATED_IMAGE line
    for line in lines:
        if line.startswith('ANNOTATED_IMAGE:'):
            annotated_image = line.split(':',1)[1].strip()
            break
    
    return {
        'answer': answer,
        'confidence': confidence,
        'analysis': analysis[:300],  # Limit to 300 chars
        'suspicious_regions': suspicious_regions[:300],
        'annotated_image': annotated_image,
        'full_response': response_text
    }
