from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)

    if file:
        img = Image.open(file.stream)
        output = remove(img)

        # Save output to an in-memory file
        img_io = io.BytesIO()
        output.save(img_io, 'PNG')
        img_io.seek(0)

        # Return the image as an attachment for download
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='output.png')


@app.route('/reset')
def reset():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
