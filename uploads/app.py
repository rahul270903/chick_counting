from flask import Flask, render_template, request, redirect, url_for
import os
from yolo_detection import count_chicks

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

@app.route('/')
def index():
    return render_template('index.html', result=None)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        file.save(image_path)

        chick_count = count_chicks(image_path)

        result_image_path = os.path.join(app.config['STATIC_FOLDER'], 'result_image.jpg')
        # Perform chick counting and save the result image
        # ...

        return render_template('index.html', result=chick_count, result_image='result_image.jpg')

if __name__ == '__main__':
    app.run(debug=True)
