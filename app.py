from flask import Flask, request, render_template, redirect, url_for, session
import os
import uuid

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Asegúrate de usar una clave secreta segura
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

comments = []

@app.route('/')
def home():
    current_user = session.get('username')
    return render_template('index.html', comments=comments, current_user=current_user)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    username = request.form.get('username')
    comment = request.form.get('comment')
    image = request.files.get('image')
    
    if username:
        session['username'] = username

    if comment:
        comment_data = {'id': str(uuid.uuid4()), 'username': username, 'text': comment, 'image_url': None}
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            comment_data['image_url'] = url_for('static', filename=f'uploads/{image.filename}')
        comments.append(comment_data)
    return redirect(url_for('home'))

@app.route('/delete_comment/<comment_id>', methods=['POST'])
def delete_comment(comment_id):
    global comments
    current_user = session.get('username')
    comments = [comment for comment in comments if comment['id'] != comment_id or comment['username'] != current_user]
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

