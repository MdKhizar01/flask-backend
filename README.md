# Flask Text, PDF, and Image Conversion API

Original standalone backend for the Techtones project. Converts text, PDFs, and images into MP3 speech using Flask, gTTS, PDF text extraction, and Tesseract OCR.

## Run

Install Python, Tesseract OCR, and the packages in requirements.txt:

```bash
python -m pip install -r requirements.txt
python app.py
```

The development server listens on port 5000. Speech conversion requires internet access; OCR requires Tesseract on PATH.

The existing Dockerfile installs Tesseract and starts Gunicorn:

```bash
docker build -t techtones-backend .
docker run --rm -p 5000:5000 techtones-backend
```

## API

- GET / — service greeting.
- POST /convert_text — JSON with a text field.
- POST /convert_pdf — multipart file field containing a PDF.
- POST /convert_image — multipart file field containing a PNG/JPG/JPEG.
- GET /static/audio/<filename> — generated MP3.

Conversion responses include an audio_path field.

## Relationship to Techtones

This is an earlier standalone conversion backend. The [Techtones repository](https://github.com/MdKhizar01/Techtones) also contains database-backed audio history and registration/login endpoints. The two implementations are retained separately because their functionality differs.

Original source is on the default master branch. Generated audio and Python caches have been removed from the current tree; Git history remains. OCR/speech endpoints and Docker builds were not rerun during portfolio cleanup.
