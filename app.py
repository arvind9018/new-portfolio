from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import bleach
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Replace with secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'arvindkumar18320@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'your-app-password'  # Replace with Gmail app password
app.config['SOCIAL_LINKS'] = {
    'github': 'https://github.com/arvind9018',
    'linkedin': 'https://linkedin.com/in/arvind-kumar-9b898b247/',
    'instagram': 'https://instagram.com/arvind.yadav.07'
}

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
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

# Context Processor for Image Fallback
@app.context_processor
def utility_processor():
    def get_image_path(filename):
        default_image = "static/images/default.jpg"
        if not filename:
            return default_image
        path = f"static/images/{filename}"
        return path if os.path.exists(os.path.join(app.root_path, path)) else default_image
    return dict(get_image_path=get_image_path)

# Routes
@app.route('/')
def home():
    posts = Post.query.order_by(Post.date.desc()).limit(3).all()
    Certifications = Certification.query.limit(3).all()
    projects = [
        {
            'title': 'E-commerce Platform',
            'description': 'A full-featured online store with payment integration and admin dashboard.',
            'image': 'project1.jpg',
            'tags': ['Flask', 'SQLAlchemy', 'Stripe API', 'Tailwind CSS'],
            'demo': '#',
            'github': '#'
        },
        {
            'title': 'Data Visualization Dashboard',
            'description': 'Interactive dashboard for exploring and visualizing complex datasets.',
            'image': 'project2.jpg',
            'tags': ['Python', 'Pandas', 'Plotly', 'Flask'],
            'demo': '#',
            'github': '#'
        },
        {
            'title': 'Portfolio Website',
            'description': 'A responsive personal portfolio website built with Flask and Tailwind CSS.',
            'image': 'project3.jpg',
            'tags': ['Flask', 'Tailwind', 'JavaScript', 'GSAP'],
            'demo': '#',
            'github': '#'
        }
    ]
    education = [
        {
            'title': 'Bachelor of Technology in Computer Science',
            'institution': 'Lovely Professional University',
            'location': 'Jalandhar, Punjab, India',
            'duration': '2020 - 2024'
        },
        {
            'title': 'High School (12th Grade)',
            'institution': 'Kendriya Vidyalaya',
            'location': 'Jalandhar, Punjab, India',
            'duration': '2018 - 2020'
        }
    ]
    return render_template('home.html', posts=posts, certifications=Certifications, projects=projects, education=education)

@app.route('/projects')
def projects():
    projects = [
        {
            'title': 'E-commerce Platform',
            'description': 'A full-featured online store with payment integration and admin dashboard.',
            'image': 'project1.jpg',
            'tags': ['Flask', 'SQLAlchemy', 'Stripe API', 'Tailwind CSS'],
            'demo': '#',
            'github': '#'
        },
        {
            'title': 'Data Visualization Dashboard',
            'description': 'Interactive dashboard for exploring and visualizing complex datasets.',
            'image': 'project2.jpg',
            'tags': ['Python', 'Pandas', 'Plotly', 'Flask'],
            'demo': '#',
            'github': '#'
        },
        {
            'title': 'Portfolio Website',
            'description': 'A responsive personal portfolio website built with Flask and Tailwind CSS.',
            'image': 'project3.jpg',
            'tags': ['Flask', 'Tailwind', 'JavaScript', 'GSAP'],
            'demo': '#',
            'github': '#'
        },
        {
            'title': 'Task Management App',
            'description': 'A productivity app for managing tasks with teams and deadlines.',
            'image': 'project4.jpg',  # Changed to avoid duplicate
            'tags': ['Django', 'PostgreSQL', 'React'],
            'demo': '#',
            'github': '#'
        },
        {
            'title': 'Weather Forecast App',
            'description': 'Real-time weather forecasting application with location detection.',
            'image': 'project5.jpg',  # Changed to avoid duplicate
            'tags': ['JavaScript', 'API Integration', 'Geolocation'],
            'demo': '#',
            'github': '#'
        },
        {
            'title': 'Recipe Finder',
            'description': 'Discover recipes based on ingredients you have at home.',
            'image': 'project6.jpg',  # Changed to avoid duplicate
            'tags': ['React', 'Node.js', 'MongoDB'],
            'demo': '#',
            'github': '#'
        }
    ]
    return render_template('projects.html', projects=projects)

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
    certifications = Certification.query.all()
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
    return render_template('contact.html', success='success' in request.args)

# Initialize Database
with app.app_context():
    db.create_all()
    if not Post.query.first() and not Certification.query.first():
        sample_posts = [
            Post(
                title='My First Blog Post',
                date=datetime(2025, 7, 1),
                image='my.jpg',
                category='Web Development',
                excerpt='An introduction to my journey in web development.',
                content=bleach.clean('<p>This is a sample blog post content about web development.</p>', tags=['p', 'h1', 'h2', 'a', 'strong'], attributes={'a': ['href']})
            ),
            Post(
                title='Data Science Insights',
                date=datetime(2025, 7, 5),
                image='blog2.jpg',
                category='Data Science',
                excerpt='Exploring data visualization techniques with Python.',
                content=bleach.clean('<p>This post covers Pandas, Matplotlib, and more.</p>', tags=['p', 'h1', 'h2', 'a', 'strong'], attributes={'a': ['href']})
            ),
            Post(
                title='Building APIs with Flask',
                date=datetime(2025, 7, 10),
                image='blog3.jpg',
                category='Web Development',
                excerpt='A guide to creating RESTful APIs using Flask.',
                content=bleach.clean('<p>Learn how to build APIs with Flask and SQLAlchemy.</p>', tags=['p', 'h1', 'h2', 'a', 'strong'], attributes={'a': ['href']})
            )
        ]
        sample_certs = [
            Certification(
                title='Google Data Analytics',
                issuer='Google',
                image='cert1.jpg',
                description='Professional certification in data analysis and visualization',
                date='July 2024',
                url='https://example.com/certificate1'
            ),
            Certification(
                title='React Frontend Developer',
                issuer='Meta',
                image='cert2.jpg',
                description='Certification in modern React development',
                date='August 2024',
                url='https://example.com/certificate2'
            ),
            Certification(
                title='Python Developer',
                issuer='Python Institute',
                image='cert3.jpg',
                description='Certified Python programmer with specialization in web development',
                date='September 2024',
                url='https://example.com/certificate3'
            )
        ]
        db.session.add_all(sample_posts + sample_certs)
        db.session.commit()
@app.route('/reset_db')
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        sample_posts = [
            Post(
                title='My First Blog Post',
                date=datetime(2025, 7, 1),
                image='my.jpg',
                category='Web Development',
                excerpt='An introduction to my journey in web development.',
                content=bleach.clean('<p>This is a sample blog post content about web development.</p>', tags=['p', 'h1', 'h2', 'a', 'strong'], attributes={'a': ['href']})
            ),
            Post(
                title='Data Science Insights',
                date=datetime(2025, 7, 5),
                image='blog2.jpg',
                category='Data Science',
                excerpt='Exploring data visualization techniques with Python.',
                content=bleach.clean('<p>This post covers Pandas, Matplotlib, and more.</p>', tags=['p', 'h1', 'h2', 'a', 'strong'], attributes={'a': ['href']})
            ),
            Post(
                title='Building APIs with Flask',
                date=datetime(2025, 7, 10),
                image='blog3.jpg',
                category='Web Development',
                excerpt='A guide to creating RESTful APIs using Flask.',
                content=bleach.clean('<p>Learn how to build APIs with Flask and SQLAlchemy.</p>', tags=['p', 'h1', 'h2', 'a', 'strong'], attributes={'a': ['href']})
            )
        ]
        sample_certs = [
            Certification(
                title='Google Data Analytics',
                issuer='Google',
                image='cert1.jpg',
                description='Professional certification in data analysis and visualization',
                date='July 2024',
                url='https://example.com/certificate1'
            ),
            Certification(
                title='React Frontend Developer',
                issuer='Meta',
                image='cert2.jpg',
                description='Certification in modern React development',
                date='August 2024',
                url='https://example.com/certificate2'
            ),
            Certification(
                title='Python Developer',
                issuer='Python Institute',
                image='cert3.jpg',
                description='Certified Python programmer with specialization in web development',
                date='September 2024',
                url='https://example.com/certificate3'
            )
        ]
        db.session.add_all(sample_posts + sample_certs)
        db.session.commit()
    return "Database reset and sample data added."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))