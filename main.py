from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
from collections import Counter
import os

app = Flask(__name__)


def get_top_colors(image_path, num_colors=10):
    try:
        img = Image.open(image_path)
        img.verify()
    except (IOError, SyntaxError):
        return jsonify({"error": "Invalid image file"}), 400
    img = img.resize((100, 100))
    img = img.convert('RGB')
    pixels = np.array(img).reshape(-1, 3)
    counter = Counter(map(tuple, pixels))
    top_colors = counter.most_common(num_colors)
    return [{"color": f"#{r:02x}{g:02x}{b:02x}", "count": count} for (r, g, b), count in top_colors]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    image = request.files['image']
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400

    image_path = os.path.join("uploads", image.filename)
    image.save(image_path)

    top_colors = get_top_colors(image_path)

    os.remove(image_path)

    return jsonify(top_colors)


if __name__ == '__main__':
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)

