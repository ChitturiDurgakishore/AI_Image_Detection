# Quick Start: Running the AI Image Detector

## Prerequisites
- Python 3.8+
- Google Gemini API key (get from: https://makersuite.google.com/app/apikey)

## Steps

### 1. Configure API Key
Edit `.env` file:
```
GEMINI_API_KEY=your-actual-api-key-from-google
```

### 2. Install Dependencies
```bash
#  Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Install packages
pip install -r requirements.txt
```

### 3. Run Server
```bash
python manage.py migrate
python manage.py runserver
```

Visit: **http://localhost:8000**

## File Summary

| File | Purpose |
|------|---------|
| `detector/views.py` | Handles image upload and response |
| `detector/gemini_service.py` | Calls Google Gemini Vision API |
| `detector/templates/detector/index.html` | Upload form and result display |
| `detector/urls.py` | URL routing for the app |
| `aidetection_project/settings.py` | Django configuration |
| `.env` | API key storage |

Done! The app is ready to detect AI-generated images.
