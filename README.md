# my-personal-portfolio
# 🚀 Arvind's Developer Portfolio

Welcome to my modern developer portfolio built using **Flask**, **Tailwind CSS**, **JavaScript**, and **SQLAlchemy**. The project includes animations, dark/light mode toggle, AOS effects, and a functional contact form that sends emails via Gmail SMTP.

🌐 **Live Site**: [arvind-new-portfolio.onrender.com](https://arvind-new-portfolio.onrender.com/)

---

## 📸 Features

- Modern UI/UX with Tailwind CSS & AOS animation
- Full dark/light mode toggle
- Projects, skills, blogs, and education sections
- Contact form with email functionality using Flask-Mail
- Embedded Google Maps
- Fully responsive (mobile, tablet, desktop)
- Hosted on [Render](https://render.com/)

---

## 🛠️ Tech Stack

- **Frontend:** HTML, Tailwind CSS, JavaScript, AOS.js
- **Backend:** Python (Flask)
- **Database:** SQLite (via SQLAlchemy)
- **Email:** Flask-Mail (Gmail SMTP)
- **Hosting:** Render (Free Tier)

---


## 🚀 Getting Started Locally

### 1. Clone the Repo
git clone https://github.com/yourusername/portfolio-flask-tailwind.git
cd portfolio-flask-tailwind

-------------------------------
2. Set Up Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

-------------------------------
3. Install Python Dependencies
pip install -r requirements.txt
-------------------------------
4. Install Node.js Dependencies (for Tailwind)
npm install


-------------------------------
5. Run Tailwind in Watch Mode
npx tailwindcss -i static/src/input.css -o static/css/output.css --watch
Make sure input.css contains the Tailwind directives:

css
@tailwind base;
@tailwind components;
@tailwind utilities;
-----------------------

6. Configure Environment Variables
Create a .env file and add:
#if u want than u also apply this method 
#.env
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password   # from Gmail App Passwords

7. Run the Flask App
python app.py
Then visit: http://127.0.0.1:5000/

---------------------------
📦 Deployment 
Deployed on: Render
To deploy:

1.Push code to GitHub
2.Connect the repo to Render

3.Set build command:
npm install && npx tailwindcss -i static/src/input.css -o static/css/output.css

4.Set start command:
gunicorn app:app
Add environment variables (e.g., MAIL_USERNAME, MAIL_PASSWORD)

-----------------------
📬 Contact
📧 Email: arvindkumar18320@gmail.com
📍 Location: Nawanshahr, Punjab, India

-----------------------
❤️ Acknowledgements
Flask

Tailwind CSS

AOS (Animate on Scroll)

Render Hosting

------------------------
📝 License
This project is licensed under the MIT License.
Would you like me to generate this as a downloadable `README.md` file or help publish it to your GitHub repo?
