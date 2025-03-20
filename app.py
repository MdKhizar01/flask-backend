from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from gtts import gTTS
import PyPDF2
from PIL import Image
import pytesseract
import os
import uuid

app = Flask(__name__)
CORS(app)

# Set up the path for static files
app.config['UPLOAD_FOLDER'] = 'static/audio'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Root route (home)
@app.route('/')
def home():
    return "Welcome to the Flask App! You can convert text, PDF, or image to audio."

# Convert Text to Audio
@app.route('/convert_text', methods=['POST'])
def convert_text():
    try:
        text = request.json['text']
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        tts = gTTS(text)
        
        # Generate a unique filename for each audio file
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        tts.save(audio_path)
        
        return jsonify({"message": "Text converted to audio successfully", "audio_path": f"/static/audio/{audio_filename}"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error converting text to audio: {str(e)}"}), 500

# Convert PDF to Audio (extract text from PDF)
@app.route('/convert_pdf', methods=['POST'])
def convert_pdf():
    try:
        file = request.files['file']
        
        if not file or not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Invalid file format. Please upload a PDF file."}), 400
        
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        
        if not text:
            return jsonify({"error": "No text found in the PDF."}), 400
        
        tts = gTTS(text)
        
        # Generate a unique filename for each audio file
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        tts.save(audio_path)
        
        return jsonify({"message": "PDF converted to audio successfully", "audio_path": f"/static/audio/{audio_filename}"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error converting PDF to audio: {str(e)}"}), 500

# Convert Image to Audio (OCR)
@app.route('/convert_image', methods=['POST'])
def convert_image():
    try:
        file = request.files['file']
        
        if not file or not file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            return jsonify({"error": "Invalid file format. Please upload a valid image (PNG, JPG, JPEG)."}), 400
        
        img = Image.open(file)
        text = pytesseract.image_to_string(img)
        
        if not text:
            return jsonify({"error": "No text found in the image."}), 400
        
        tts = gTTS(text)
        
        # Generate a unique filename for each audio file
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
        tts.save(audio_path)
        
        return jsonify({"message": "Image converted to audio successfully", "audio_path": f"/static/audio/{audio_filename}"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error converting image to audio: {str(e)}"}), 500

# Serve audio files
@app.route('/static/audio/<filename>')
def serve_audio(filename):
    try:
        return send_from_directory(os.path.join(app.root_path, 'static', 'audio'), filename)
    except Exception as e:
        return jsonify({"error": f"Error serving audio file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
