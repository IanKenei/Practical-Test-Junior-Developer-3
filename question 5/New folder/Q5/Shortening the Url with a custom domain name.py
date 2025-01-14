from flask import Flask, request, redirect, render_template_string
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(200), unique=True, nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for i in range(6))
    return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        custom_domain = request.form['custom_domain']
        
        if custom_domain:
            short_url = custom_domain
        else:
            short_url = generate_short_url()

        new_url = URL(original_url=original_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()
        return render_template_string('Shortened URL: <a href="{{ short_url }}">{{ short_url }}</a>', short_url=short_url)

    return '''
        <form method="post">
            URL: <input type="text" name="url" required><br>
            Custom Domain (optional): <input type="text" name="custom_domain"><br>
            <input type="submit" value="Shorten URL">
        </form>
    '''

@app.route('/<short_url>')
def redirect_to_original(short_url):
    url_entry = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(url_entry.original_url)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)