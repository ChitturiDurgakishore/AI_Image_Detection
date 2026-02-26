# 🤖 AI Image Detection System

A Django-based web application that detects whether uploaded images are AI-generated or real using Google Gemini 3 Flash Vision API with intelligent circle annotations highlighting suspicious regions.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Architecture](#architecture)
5. [Project Structure](#project-structure)
6. [Setup Instructions](#setup-instructions)
7. [How It Works](#how-it-works)
8. [API Endpoints](#api-endpoints)
9. [File Descriptions](#file-descriptions)
10. [Troubleshooting](#troubleshooting)
11. [Future Enhancements](#future-enhancements)

---

## 🎯 Project Overview

This system analyzes uploaded images to determine if they are AI-generated or real photographs. It uses Google's Gemini 3 Flash Vision API to perform deep image analysis and provides:

- **Classification**: AI-generated or Real
- **Confidence Level**: High/Medium/Low
- **Detailed Analysis**: 2-3 sentence explanation of findings
- **Suspicious Regions**: Specific areas where AI artifacts are detected
- **Visual Annotations**: Orange circles drawn on detected problematic areas for easy comparison

---

## ✨ Features

### Core Detection
- ✅ AI vs Real image classification
- ✅ Confidence scoring (High/Medium/Low)
- ✅ Detailed analysis report from Gemini API
- ✅ Specific suspicious region identification

### Visual Comparison
- ✅ **Side-by-side original vs annotated** images
- ✅ Orange circles highlighting detected AI artifacts
- ✅ Smart region mapping (eyes, hands, face, background, etc.)
- ✅ Responsive, mobile-friendly UI

### Image Processing
- ✅ Automatic image resizing (max 1024px to avoid timeouts)
- ✅ Format conversion (RGBA/PNG → RGB/JPEG)
- ✅ Quality optimization (JPEG quality 85)
- ✅ Support for JPEG, PNG, GIF, WebP

### User Experience
- ✅ Real-time file preview
- ✅ Loading indicator during analysis
- ✅ Error display and debugging info
- ✅ Raw Gemini response display for transparency
- ✅ Clean, modern, gradient-based UI

---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 4.2.8 | Web framework |
| **Python** | 3.8+ | Programming language |
| **Google Generative AI** | 0.3.1+ | Gemini Vision API client |
| **Pillow** | 10.1.0 | Image processing (resize, convert, annotate) |
| **python-dotenv** | 1.0.0 | Environment variable management |
| **SQLite** | Built-in | Database (lightweight) |

### Frontend
- **HTML5** – Structure
- **CSS3** – Modern styling with CSS variables, gradients, animations
- **Vanilla JavaScript** – Client-side interactivity (no frameworks)

### API
- **Google Gemini 3 Flash Preview** – Vision API for image analysis
  - Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent`
  - Model: `gemini-3-flash-preview`
  - Why: Fast, cost-effective, excellent at fast image analysis

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Browser                              │
│  (HTML/CSS/JS - Modern UI with side-by-side comparison)         │
└────────────────────────┬────────────────────────────────────────┘
                         │
                    POST /upload
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   Django Views (views.py)                        │
│                                                                  │
│  1. Receive image file                                          │
│  2. Call gemini_service.analyze_image()                        │
│  3. Generate local circle overlay (add_analysis_overlay())     │
│  4. Render template with results                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
  [Image Processing]  [Gemini API]  [Response Parsing]
        │                │                │
┌───────▼─────────────────▼────────────────▼───────────┐
│         gemini_service.analyze_image()               │
│                                                      │
│  1. Resize image to max 1024px (avoid 504)          │
│  2. Convert RGBA/GIF → RGB (JPEG compatible)        │
│  3. Send to Gemini 3 Flash API with prompt          │
│  4. Parse classification, confidence, analysis      │
│  5. Extract suspicious regions                      │
│  6. Return structured JSON response                 │
└───────────────────────┬──────────────────────────────┘
                        │
           ┌────────────▼──────────────┐
           │  Google Gemini API        │
           │  (Cloud-based analysis)   │
           └──────────────────────────┘
                        │
        ┌───────────────▼────────────────┐
        │  Response:                      │
        │  - CLASSIFICATION: AI/Real     │
        │  - CONFIDENCE: High/Med/Low    │
        │  - ANALYSIS: Text              │
        │  - SUSPICIOUS_REGIONS: Text    │
        └──────────────────────────────┘
```

---

## 📁 Project Structure

```
AIDETECTION/
├── manage.py                              # Django management script
├── requirements.txt                       # Python dependencies
├── .env                                   # API key (GitHub excluded)
├── .gitignore                             # Git ignore patterns
├── README.md                              # This file
├── QUICKSTART.md                          # Quick 5-minute setup
├── SETUP_INSTRUCTIONS.md                  # Detailed documentation
│
├── aidetection_project/                   # Project settings
│   ├── __init__.py
│   ├── settings.py                        # Django configuration
│   ├── urls.py                            # Main URL routing
│   ├── wsgi.py                            # WSGI application
│
└── detector/                              # Main Django app
    ├── migrations/                        # Database migrations
    │   └── __init__.py
    ├── templates/
    │   └── detector/
    │       └── index.html                 # Main page template (310 lines)
    ├── __init__.py
    ├── admin.py                           # Django admin configuration
    ├── apps.py                            # App configuration
    ├── gemini_service.py                  # Gemini API wrapper (129 lines)
    ├── models.py                          # Database models
    ├── tests.py                           # Unit tests
    ├── urls.py                            # App URL routing
    └── views.py                           # Request handlers (135 lines)
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or newer
- Google Gemini API key (free tier available)
- 100+ MB free disk space

### Step 1: Get API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"** or use existing
3. Copy the key (looks like: `AIza...`)

### Step 2: Clone/Setup Project
```bash
cd c:\Major_Project\AIDETECTION
```

### Step 3: Create Virtual Environment
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

The following packages are installed:
```
Django==4.2.8                    # Web framework
google-generativeai==0.3.1       # Gemini API client
python-dotenv==1.0.0            # Environment variables
Pillow==10.1.0                   # Image processing
```

### Step 5: Configure API Key
Edit `.env` file in project root:
```
GEMINI_API_KEY=AIza_YOUR_ACTUAL_KEY_HERE
```

### Step 6: Initialize Database
```bash
python manage.py migrate
```

### Step 7: Run Development Server
```bash
python manage.py runserver

# Or specify a different port
python manage.py runserver 8001
```

Server runs at: **http://localhost:8000**

---

## 🔍 How It Works

### Step-by-Step Flow

#### 1️⃣ **Upload Image** (Client-side)
- User selects image via file picker or drag-and-drop
- Browser shows instant preview
- Filename displayed below upload box

#### 2️⃣ **Image Processing** (Backend - views.py)
```python
# Original image stored as-is (for comparison)
original_src = base64-encoded original

# Analysis triggered
result = analyze_image(image_file)

# Circled overlay generated locally
circled_src = add_analysis_overlay(image_file, result)
```

#### 3️⃣ **Gemini Analysis** (gemini_service.py)
```
a) Resize image to 1024px max
   └─ Prevents 504 timeouts, reduces processing time

b) Convert format (RGBA → RGB)
   └─ Ensures JPEG compatibility

c) Send to Gemini 3 Flash API
   └─ Model: gemini-3-flash-preview
   └─ Prompt: Classification task with structured output

d) Parse response
   └─ Extract: Classification, Confidence, Analysis, Suspicious_Regions
   └─ Return as JSON
```

#### 4️⃣ **Circle Annotation** (views.py - add_analysis_overlay)
```python
for each suspicious_region keyword:
  map to image location:
    - 'eye'/'eyes'     → (0.3, 0.2)  # Upper left
    - 'face'           → (0.5, 0.3)  # Upper center
    - 'hand'/'hands'   → (0.7, 0.6)  # Lower right
    - 'background'     → (0.5, 0.5)  # Center
    - 'mouth'          → (0.5, 0.35) # Center-top
    - 'texture'        → (0.4, 0.6)  # Center-left
    
  draw orange circle at location
    └─ Color: RGB(255, 152, 0) with transparency
    └─ Radius: 20-100px depending on image size
```

#### 5️⃣ **Display Results** (template)
- **Left panel**: Original uploaded image (unchanged)
- **Right panel**: Same image with orange circles on detected areas
- **Analysis box**: Classification, confidence, detailed findings
- **Raw output**: Full Gemini response (for debugging)

---

## 📡 API Endpoints

### Main Endpoint
| Method | URL | Purpose |
|--------|-----|---------|
| **GET** | `/` | Render upload page |
| **POST** | `/` | Process image upload |

### Response Format
```python
{
    'result': 'AI' or 'Real' or 'Unknown',
    'confidence': 'High' or 'Medium' or 'Low',
    'analysis': '2-3 sentence explanation',
    'suspicious_regions': 'List of detected problem areas',
    'full_response': 'Raw Gemini output (for debugging)',
    'original_src': 'base64-encoded original image',
    'circled_src': 'base64-encoded image with circles',
    'annotated_src': 'Gemini-provided annotated image (if available)'
}
```

### External API: Google Gemini
```
Endpoint: https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent
Method: POST
Auth: x-goog-api-key header
Input: Image (base64) + text prompt
Output: JSON with generated analysis text
Rate Limit: See Google's quota docs
```

---

## 📄 File Descriptions

### Core Files

#### `detector/gemini_service.py` (129 lines)
**Purpose**: Handles all communication with Google Gemini API

**Key Functions**:
- `analyze_image(image_file)` – Main analysis function
  - Resizes image to 1024px max
  - Converts RGBA → RGB
  - Sends to Gemini 3 Flash API
  - Parses structured response
  - Returns classification + analysis

**Prompt Used**:
```
"Analyze this image and determine if it's AI-generated or real.
Respond in this exact format:
CLASSIFICATION: AI or Real
CONFIDENCE: High/Medium/Low
ANALYSIS: 2-3 sentence explanation
SUSPICIOUS_REGIONS: Specific problem areas..."
```

#### `detector/views.py` (135 lines)
**Purpose**: Django view handling HTTP requests and responses

**Key Functions**:
- `index(request)` – Main view
  - Receives uploaded image
  - Calls `analyze_image()`
  - Generates original + circled versions
  - Renders template with results

- `add_analysis_overlay(image_file, result)` – Draws circles
  - Creates PIL Image copy
  - Maps keywords to image locations
  - Draws orange circles
  - Returns base64-encoded PNG

#### `detector/urls.py` (5 lines)
**Purpose**: URL routing for the detector app
```python
urlpatterns = [
    path('', views.index, name='index'),
]
```

#### `detector/templates/detector/index.html` (310 lines)
**Purpose**: User interface template

**Sections**:
- Header with title and subtitle
- Two-column image comparison (original vs circled)
- File upload form with drag-and-drop
- Analysis results panel (classification, confidence, analysis)
- Debug section (raw Gemini response)

**Styling**:
- CSS variables for theming
- Gradient backgrounds
- Smooth animations (slide-in, fade-in, zoom)
- Responsive grid layout
- Mobile-friendly media queries

**JavaScript**:
- File preview on select
- Drag-and-drop support
- Loading indicator
- Form submission handling

#### `aidetection_project/settings.py` (60+ lines)
**Purpose**: Django configuration

**Key Settings**:
```python
INSTALLED_APPS = ['detector']
TEMPLATES = [App directory templates]
DATABASES = SQLite3
MEDIA_ROOT = 'media/' (for uploads)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

#### `aidetection_project/urls.py` (12 lines)
**Purpose**: Main project URL routing
```python
urlpatterns = [
    path('', include('detector.urls')),
]
```

#### `.env` (1 line)
**Purpose**: Environment variables (GitHub excluded)
```
GEMINI_API_KEY=AIza_YOUR_KEY
```

#### `requirements.txt` (4 lines)
**Purpose**: Python dependency specification
```
Django==4.2.8
google-generativeai==0.3.1
python-dotenv==1.0.0
Pillow==10.1.0
```

---

## 🚨 Troubleshooting

### Problem: 504 Deadline Exceeded
**Cause**: Image too large or API timeout

**Solution**:
- ✅ Already fixed! Code now resizes images to 1024px max
- Reduces processing time significantly

### Problem: "Cannot write mode RGBA as JPEG"
**Cause**: PNG with transparency being saved as JPEG

**Solution**:
- ✅ Already fixed! Code converts RGBA → RGB before JPEG save
- Background filled with white

### Problem: "GEMINI_API_KEY environment variable not set"
**Cause**: `.env` file missing or API key not configured

**Solution**:
1. Create `.env` file in project root
2. Add: `GEMINI_API_KEY=AIza_your_key`
3. Restart server

### Problem: "ModuleNotFoundError: No module named 'dotenv'"
**Cause**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

### Problem: Quote exceeded (429 error)
**Cause**: Free tier rate limit reached

**Solution**:
- Wait a few minutes
- Check [Google AI quotas](https://ai.dev/rate-limit)
- Upgrade to paid tier if needed

### Problem: Page just refreshes, no results shown
**Cause**: An error occurred but wasn't visible

**Solution**:
- Look for error box at top of results panel
- Check raw Gemini response (at bottom)
- Open browser console (F12) for JavaScript errors

---

## 🔮 Future Enhancements

### Planned Features
- [ ] **Database storage** – Save analysis history
- [ ] **Admin dashboard** – View past analyses
- [ ] **Batch processing** – Upload multiple images
- [ ] **PDF reports** – Generate detection reports
- [ ] **API endpoint** – JSON API for external tools
- [ ] **Model comparison** – Switch between different Vision APIs
- [ ] **Advanced filtering** – Filter by confidence, date, etc.
- [ ] **Download annotations** – Save circled images locally
- [ ] **WebSocket** – Real-time streaming analysis
- [ ] **Docker deployment** – Containerized setup

### Possible Improvements
- Switch to `gemini-2.0-pro` for higher accuracy (if quota allows)
- Add more sophisticated circle placement (ML-based)
- Implement image caching to avoid re-analysis
- Add user authentication for multi-user support
- Create mobile app version

---

## 📞 Support

### Resources
- [Django Docs](https://docs.djangoproject.com/)
- [Google Generative AI Docs](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/api/rest)
- [Pillow Image Processing](https://pillow.readthedocs.io/)

### Common Use Cases

**Want to analyze batch of images?**
- Modify `views.py` to accept multiple files
- Loop through each, call `analyze_image()`, store results

**Want to switch to different model?**
- Edit `detector/gemini_service.py` line 71
- Change: `genai.GenerativeModel('gemini-2.0-pro')`

**Want to customize circle placement?**
- Edit `add_analysis_overlay()` mapping dictionary in `views.py`
- Add more keywords and coordinates

---

## 📄 License

This project is open-source and available for educational and commercial use.

---

## 🎉 Summary

| Aspect | Details |
|--------|---------|
| **Language** | Python 3.8+ |
| **Framework** | Django 4.2 |
| **Vision API** | Google Gemini 3 Flash Preview |
| **Image Processing** | Pillow (PIL) |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3, Vanilla JS |
| **Status** | ✅ Fully Functional |
| **Setup Time** | ~5 minutes |
| **First Image Analysis** | ~5-10 seconds |

---

**Last Updated:** February 26, 2026  
**Version:** 1.0.0  
**Status:** Production Ready
