from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import bleach
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'arvindkumar18320@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'nlzk tdrm zdgn vthp'  # Use Gmail App Password

# Social links config
app.config['SOCIAL_LINKS'] = {
    'github': 'https://github.com/arvind9018',
    'linkedin': 'https://linkedin.com/in/arvind-kumar-9b898b247/',
    'instagram': 'https://instagram.com/arvind.yadav.07'
}

db = SQLAlchemy(app)
mail = Mail(app)

# ========== Models ==========

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(50), nullable=False)
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=True)

class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    issuer = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(200), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    tech_stack = db.Column(db.String(200), nullable=False)
    demo = db.Column(db.String(200), nullable=True)   # ✅ New field
    github = db.Column(db.String(200), nullable=True) # ✅ New field
    category = db.Column(db.String(50), nullable=False)


# ========== Utilities ==========

@app.context_processor
def utility_processor():
    def get_image_path(filename):
        default_image = "static/images/default.jpg"
        if not filename:
            return default_image
        path = f"static/images/{filename}"
        return path if os.path.exists(os.path.join(app.root_path, path)) else default_image
    return dict(get_image_path=get_image_path)

# ========== Routes ==========

@app.route('/')
def home():
    posts = Post.query.order_by(Post.date.desc()).limit(3).all()
    certifications = Certification.query.order_by(Certification.id.desc()).limit(3).all()
    projects = Project.query.order_by(Project.id.desc()).limit(3).all()
    education = [
        {
        'title': 'Bachelor of Technology in Computer Science',
        'institution': 'Lovely Professional University',
        'location': 'Phagwara, Punjab, India',
        'duration': '2022 - 2026'
    },
    {
        'title': 'Senior Secondary (12th Grade)',
        'institution': 'Govt. Senior Secondary School',
        'location': 'Nawanshahr, Punjab, India',
        'duration': '2019 - 2020'
    },
    {
        'title': 'Matriculation (10th Grade)',
        'institution': 'Govt. Senior Secondary School',
        'location': 'Nawanshahr, Punjab, India',
        'duration': '2017 - 2018'
    }
    ]
    return render_template('home.html', posts=posts, certifications=certifications, projects=projects, education=education)

@app.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.id.desc()).all()
    return render_template('projects.html', projects=all_projects)

@app.route('/blog')
def blog():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

@app.route('/certifications')
def certifications_page():
    certifications = Certification.query.order_by(Certification.id.desc()).all()
    return render_template('certifications.html', certifications=certifications)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        try:
            msg = Message('Contact Form Submission', sender=email, recipients=['arvindkumar18320@gmail.com'])
            msg.body = f"From: {name}\nEmail: {email}\nMessage: {message}"
            mail.send(msg)
            flash('Your message has been sent. I\'ll get back to you soon.', 'success')
        except Exception as e:
            flash('Error sending message. Please try again later.', 'error')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ========== Reset DB ==========

@app.route('/reset_db')
def reset_db():
    db.drop_all()
    db.create_all()

    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

            for item in data.get('posts', []):
                post = Post(
                    title=item['title'],
                    date=datetime.strptime(item['date'], '%Y-%m-%d'),
                    category=item['category'],
                    excerpt=item['excerpt'],
                    content=bleach.clean(item['content'], tags=['p', 'ul', 'li', 'h2', 'h3', 'strong', 'br', 'div', 'span'], attributes={'a': ['href']}),
                    image=item['image']
                )
                db.session.add(post)

            for item in data.get('certifications', []):
                cert = Certification(
                    title=item['title'],
                    issuer=item['issuer'],
                    image=item['image'],
                    description=item['description'],
                    date=item['date'],
                    url=item['url']
                )
                db.session.add(cert)
            
            for item in data.get('projects', []):
                project = Project(
                    title=item['title'],
                    description=item['description'],
                    image=item['image'],
                    tech_stack=item['tech_stack'],
                    demo=item.get('demo', ''),
                    github=item.get('github', ''),
                    category=item.get('category', 'other')
                )
                db.session.add(project)

            db.session.commit()
    except Exception as e:
        return f"❌ Error loading data.json: {e}"

    return "✅ Database reset and sample data loaded successfully!"

# ========== Run App ==========

if __name__ == '__main__':
    app.run(debug=True)
