# import os
# import google.generativeai as genai
# import PIL.Image
# from dotenv import load_dotenv

# # --- Load the API Key ---
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("Gemini API key not found. Please set it in the .env file.")

# # --- Configure the Gemini Client ---
# genai.configure(api_key=api_key)

# # --- Create the Model ---
# print("Loading Gemini model...")
# model = genai.GenerativeModel('gemini-2.5-flash')

# # --- Prepare Image and Prompt ---
# image = PIL.Image.open("landmark.jpg")
# prompt = "What are three interesting facts about this landmark?"

# # --- Generate Content ---
# print("Asking Gemini...")
# response = model.generate_content([prompt, image])

# # --- Display the Result ---
# print("\n--- Gemini's Response ---")
# print(response.text)
# print("-------------------------\n")

import os
import google.generativeai as genai
import PIL.Image
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# --- CONFIGURATION ---
load_dotenv()
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# --- MODEL INITIALIZATION ---
model = genai.GenerativeModel('gemini-2.5-flash')

# --- FLASK APP ---
app = Flask(__name__)

# --- ROUTES ---
@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Handles the image and prompt submission for analysis."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image_file = request.files['image']
    prompt = request.form.get('prompt', 'Describe this image.')

    try:
        image = PIL.Image.open(image_file.stream)
        response = model.generate_content([prompt, image])
        return jsonify({'text': response.text})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {e}'}), 500

# --- RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True)
    