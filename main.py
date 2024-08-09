from flask import Flask, request, render_template, redirect, url_for, send_from_directory, jsonify
import os

app = Flask(__name__)

# Configure the upload folder
UPLOAD_FOLDER = 'static/photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory storage for favorites
favorites = []

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/gallery')
def gallery_page():
    photos = [f"/static/photos/{file}" for file in os.listdir(app.config['UPLOAD_FOLDER']) if file.endswith(('png', 'jpg', 'jpeg', 'gif'))]
    return render_template('gallery.html', photos=photos)

@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('gallery_page'))

@app.route('/photos', methods=['GET'])
def get_photos():
    photos = [f"/static/photos/{file}" for file in os.listdir(app.config['UPLOAD_FOLDER']) if file.endswith(('png', 'jpg', 'jpeg', 'gif'))]
    return jsonify({"photos": photos})

@app.route('/add-to-favorites', methods=['POST'])
def add_to_favorites():
    photo_url = request.json.get('photoUrl')
    if photo_url and photo_url not in favorites:
        favorites.append(photo_url)
    return jsonify({"message": "Photo added to favorites"})

@app.route('/favorites', methods=['GET'])
def get_favorites():
    return jsonify({"favorites": favorites})

@app.route('/favorites-page')
def favorites_page():
    return render_template('favorites.html', favorites=favorites)

@app.route('/clear-favorites', methods=['POST'])
def clear_favorites():
    favorites.clear()
    return redirect(url_for('gallery_page'))

@app.route('/download/<filename>')
def download_image(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
