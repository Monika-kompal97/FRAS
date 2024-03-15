from flask import Flask, render_template, request, redirect, url_for, Response,flash
"""import cv2
import firebase_admin
from firebase_admin import credentials, auth, db,firestore,storage
import re

cred = credentials.Certificate("C:/Users/Admin/OneDrive/Desktop/Majorproject (5)/Majorproject/majorproject-550be-firebase-adminsdk-wzfdz-4b636ba1b9.json")
firebase_admin.initialize_app(cred,{
    'storageBucket':'majorproject-550be.appspot.com'
})
db=firestore.client()
bucket = storage.bucket()
app = Flask(__name__,template_folder="C:/Users/Admin/OneDrive/Desktop/Majorproject (5)/Majorproject/templates")
app.secret_key = 'Monu@143'
# camera = cv2.VideoCapture(0)  # Initialize webcam

# Dummy data for students and admins (in real-world scenarios, this data would be stored in a database)
students = []
admins = [{'username': 'admin', 'password': 'admin'}]"""
app = Flask(__name__,template_folder="C:/Users/Admin/OneDrive/Desktop/trial/templates")
app.secret_key = 'Monu@143'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


"""if __name__ == '__main__':
    app.run(debug=True)"""