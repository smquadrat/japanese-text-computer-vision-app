from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import sys
import io
import os
import base64
import pyocr
import cv2
import numpy as np
from googletrans import Translator

app = Flask(__name__)

# Set the TESSDATA_PREFIX environment variable
# Prior: os.environ["TESSDATA_PREFIX"] = "C:/Program Files/Tesseract-OCR/tessdata"
os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/"

# Initialize PyOCR and Googletrans
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
ocr_tool = tools[0]
translator = Translator()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    print('test')

    if 'file' in request.files:
        # If an image file was uploaded, process it
        file = request.files["file"]
        file_bytes = file.read()
        image = Image.open(io.BytesIO(file_bytes))
        print('clear')
    else:
        # Otherwise, use the sample image
        filename = request.args.get('filename', 'sample_image.jpg')
        image_path = os.path.join(app.root_path, 'static', filename)

        print(filename)
        print(image_path)
        print('test')

        with open(image_path, "rb") as f:
            file_bytes = f.read()
            image = Image.open(io.BytesIO(file_bytes))

    # Process the image
    translations, updated_image = recognize_and_translate(image)
    # Save the processed image
    output_buffer = io.BytesIO()
    updated_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)
    # Convert the images to base64 strings
    original_image_b64 = base64.b64encode(file_bytes).decode('ascii')
    updated_image_b64 = base64.b64encode(output_buffer.getvalue()).decode('ascii')
    # Pass the translations and the base64-encoded images to the result template
    return render_template("result.html", original_image=original_image_b64, updated_image=updated_image_b64, translations=translations)


def recognize_and_translate(image):
    # Convert the image to an OpenCV array
    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    image_gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)

    # Apply threshold to convert to black and white
    _, image_bw = cv2.threshold(image_gray, 128, 255, cv2.THRESH_BINARY_INV)

    # Apply morphology to remove noise and smooth edges
    kernel = np.ones((2, 2), np.uint8)
    image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_CLOSE, kernel)
    image_bw = cv2.morphologyEx(image_bw, cv2.MORPH_OPEN, kernel)

    # image_bw_pil = Image.fromarray(image_bw)
    # image_bw_pil.show()

    # Use PyOCR to recognize the characters
    lang = 'jpn+eng'
    builder = pyocr.builders.LineBoxBuilder(tesseract_layout=6)
    builder.tesseract_configs.append('tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    line_boxes = ocr_tool.image_to_string(Image.fromarray(image_bw), lang=lang, builder=builder)

    # Use Googletrans to translate the characters
    translations = {}
    for box in line_boxes:
        text = box.content
        translation = translator.translate(text, dest="en").text
        translations[text] = translation

    # Create a new image to draw the translated text
    font = ImageFont.truetype("arial.ttf", size=16)
    text_image_size = (image_cv2.shape[1], image_cv2.shape[0])
    text_image = Image.new("RGBA", text_image_size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_image)
    for box in line_boxes:
        text = box.content
        translated_text = translations[text]
        position = (box.position[0][0], box.position[0][1] - font.size)
        text_size = font.getsize(translated_text)
        bg_size = (text_size[0] + 10, text_size[1] + 10)
        bg_image = Image.new("RGBA", bg_size, (255, 255, 255, 255))
        bg_draw = ImageDraw.Draw(bg_image)
        bg_draw.text((5, 5), translated_text, font=font, fill=(0, 0, 0, 255))
        text_image.alpha_composite(bg_image, position)

    # Composite the translated text image onto the original image
    image_rgba = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGBA))
    image_composite = Image.alpha_composite(image_rgba, text_image)

    return translations, image_composite

if __name__ == "__main__":
    app.run(debug=True)