# UB1093
PillPal – A Flask-based medicine reminder web application with user authentication and dashboard features.
PillPal – Medicine Reminder Web Application
Project Overview
PillPal is a Flask-based healthcare web application that helps users manage and track their daily medicines. The application provides secure user authentication, profile management, and a personalized dashboard for each user.
Features
• User Registration and Login System
• Secure Password Hashing
• Profile Management
• Personalized Dashboard
• SQLite Database Integration
• Responsive Web Interface
Technologies Used
• Python 3
• Flask
• Flask-SQLAlchemy
• SQLite
• HTML5
• CSS3
Project Structure
PillPal
│
├── app.py
├── profile.py
├── requirements.txt
├── static/
│     └── style.css
├── templates/
│     ├── index.html
│     ├── login.html
│     ├── register.html
│     ├── dashboard.html
│     └── profile.html
└── README.md
Setup Instructions
Follow the steps below to run the project locally.

Step 1: Clone the Repository
Open Command Prompt or Terminal and run:
git clone https://github.com/your-username/pillpal.git�
cd pillpal
(Replace "your-username" with your actual GitHub username.)

Step 2: Create Virtual Environment (Recommended)
For Windows:
python -m venv venv
venv\Scripts\activate
For Mac/Linux:
python3 -m venv venv
source venv/bin/activate

Step 3: Install Required Dependencies
Make sure requirements.txt exists in the project folder.
pip install -r requirements.txt
If requirements.txt is not available, install manually:
pip install flask flask-sqlalchemy werkzeug

Step 4: Run the Application
python app.py

Step 5: Open in Browser
Open your browser and go to:
http://127.0.0.1:5000�
Your application should now be running successfully.
Database Information
• Database used: SQLite
• The database file is automatically created when the application runs for the first time.
• SQLAlchemy ORM is used for database operations.
Deployment (Optional)
The application can be deployed on platforms such as:
• Render
• PythonAnywhere
• Railway

For production deployment, use:
gunicorn app:app
Android Version
This web application can be converted into an Android application using WebView in Android Studio.
Security Notes
• Passwords are hashed before being stored in the database.
• Debug mode should be turned off in production environments.

License
This project is developed for educational purposes.
