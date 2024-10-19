from flask import Flask, render_template, request, url_for, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import random
import os

app = Flask(__name__)

# Define the path where the output images will be stored
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'static', 'output')

# Ensure the output folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Function to create the handwritten image using default font
def create_handwritten_image(text):
    img = Image.new('RGB', (800, 400), color='white')
    d = ImageDraw.Draw(img)

    # Use the default Pillow font (no custom font file required)
    font = ImageFont.load_default()

    x, y = 50, 150  # Starting position for the text
    for letter in text:
        # Draw each letter without additional size variation or random gaps
        d.text((x, y), letter, font=font, fill=(0, 0, 0))
        
        # Use bounding box to get the exact width of the letter to calculate position
        letter_width = d.textbbox((x, y), letter, font=font)[2]  # [2] gives the width
        x += letter_width  # Move the x position by the width of the letter

    # Limit filename to first 10 characters of text
    filename = f"{text[:10]}.png"
    
    # Save the image to the output folder
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    img.save(filepath)
    
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/generator', methods=['GET', 'POST'])
def generator():
    if request.method == 'POST':
        text = request.form['text']
        filename = create_handwritten_image(text)
        download_url = url_for('download_image', filename=filename)
        return render_template('generator.html', filename=filename, text=text, download_url=download_url)
    return render_template('generator.html')

@app.route('/download/<filename>')
def download_image(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
