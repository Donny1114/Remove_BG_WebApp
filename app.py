from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
from rembg import remove
import io
import os
import zipfile

app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY', 'your_default_secret_key_here')  # Set a secret key for session management


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_images():
    files = request.files.getlist('images')  # Get multiple files
    if not files or files[0].filename == '':
        return redirect(request.url)

    output_images = []
    for file in files:
        # Check for valid image files
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return redirect(request.url)  # Redirect back if not an image

        try:
            img = Image.open(file.stream)
            output = remove(img)

            img_io = io.BytesIO()
            output.save(img_io, 'PNG')
            img_io.seek(0)

            output_images.append(img_io)
        except Exception as e:
            # Log the error or handle it appropriately
            return redirect(request.url)  # Redirect back on error

    # If there's only one image, return it as a single file download
    if len(output_images) == 1:
        return send_file(output_images[0], mimetype='image/png', as_attachment=True, download_name='output.png')

    # If multiple images, return them as a zip file
    zip_io = io.BytesIO()
    with zipfile.ZipFile(zip_io, mode='w') as zipf:
        for i, img_io in enumerate(output_images):
            zipf.writestr(f'output_{i + 1}.png', img_io.read())

    zip_io.seek(0)
    return send_file(zip_io, mimetype='application/zip', as_attachment=True, download_name='output_images.zip')


@app.route('/reset')
def reset():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
