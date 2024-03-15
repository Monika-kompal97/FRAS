from flask import Flask, render_template, request, redirect, url_for, Response,flash
import cv2
import firebase_admin
from firebase_admin import credentials, auth, db,firestore,storage
import re
from pathlib import Path

cred = credentials.Certificate("majorproject-550be-firebase-adminsdk-wzfdz-4b636ba1b9.json")
firebase_admin.initialize_app(cred,{
    'storageBucket':'majorproject-550be.appspot.com'
})
db=firestore.client()
bucket = storage.bucket()
app = Flask(__name__,template_folder="templates")
app.secret_key = 'Monu@143'
# camera = cv2.VideoCapture(0)  # Initialize webcam

# Dummy data for students and admins (in real-world scenarios, this data would be stored in a database)
students = []
admins = [{'username': 'admin', 'password': 'admin'}]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    # ref=db.reference('/student')
   
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usn=request.form['usn']
        sem=request.form['sem']
        branch=request.form['branch']
        status='pending'

        USN=r'^2BA20CS\d{3}$'
        sem_pattern = r'^[1-8]$'
        branch_pattern = r'^[a-zA-Z\s]+$'
        username_pattern=r'^[a-zA-Z\s]+$'
        password_pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'


        # Add the student to the list of pending students (to be approved by admin)
        print(username)
        print(password)
        if not re.match(username_pattern, username):
            return render_template('register.html', error="Invalid username format. Username must be 3-20 characters long and can contain letters, numbers, and underscores only.")
        
        if not re.match(USN, usn):
            return render_template('register.html', error="Invalid USN format. USN must be 10 characters long and can contain letters and numbers only.")
        
        if not re.match(sem_pattern, sem):
            return render_template('register.html', error="Invalid semester format. Semester must be a number between 1 and 8.")
        
        if not re.match(branch_pattern, branch):
            return render_template('register.html', error="Invalid branch format. Branch can contain letters and spaces only.")
        
        if not re.match(password_pattern, password):
            return render_template('register.html', error="Invalid password format. it should contain atleast 8 characters with uppercase ,lowercase and special character .")
        d={'name':username,'password':password,'usn':usn,'sem':sem,'branch':branch,'status':status}
            # db.collection('student').add(d)
        db.collection('student').document(usn).set(d)
        students.append({'username': username, 'password': password, 'approved': False})
        # if username!="" and password!="" and usn!="" and sem!="" and branch!="":
        #     take_capture_images(usn)
        # return Response(capture_by_frames(usn), mimetype='multipart/x-mixed-replace; boundary=frame')
        # capture_by_frames(usn)
        # /get_usn(usn)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

# def get_usn(usn):
#     return usn
# def take_capture_images():
#     return Response(capture_by_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def capture_by_frames(usn):
   
    print("Monu")
    print(usn)
    global camera
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    count = 0  # Counter to track captured images
    while count < 100:
        success, frame = camera.read()
        if not success:
            continue
        faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            # Save the face image
            face_img = frame[y:y+h, x:x+w]
            filename = f"{usn}_{count}.jpg"
            cv2.imwrite(filename, face_img)
            upload_to_firebase(filename, usn)
            count += 1
            if count==100:
                camera.release()
        # Convert frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def upload_to_firebase(filename, usn):
    print("hello")
    bucket = storage.bucket()
    blob = bucket.blob(f"{usn}/{filename}")
    blob.upload_from_filename(filename)
    print(filename)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the admin credentials are correct
        if {'username': username, 'password': password} in admins:
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error=True)
    return render_template('admin_login.html', error=False)

@app.route('/video_capture')
def video_capture():
    usn = request.args.get('usn')
    """username=request.args.get('username')
    sem=request.args.get('sem')
    branch=request.args.get('branch')
    password=request.args.get('password')
    USN=r'^[2BA20CS][0-9]{3}$'
    sem_pattern = r'^[1-8]$'
    branch_pattern = r'^[a-zA-Z\s]+$'
    username_pattern=r'^[a-zA-Z\s]+$'
    password_pattern=r'^(?=.[a-z])(?=.[A-Z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$'
    if re.match(USN, usn) and re.match(username_pattern,username) and re.match(sem_pattern,sem) and re.match(password_pattern,password) and re.match(branch_pattern,branch):
            return Response(capture_by_frames(usn), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return redirect(url_for('register'))"""
    print("monika")
    return Response(capture_by_frames(usn), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/admin/dashboard')
def admin_dashboard():
    # return render_template('admin_dashboard.html', students=students)
     pending_students = db.collection('student').where('status', '==', 'pending').stream()
     return render_template('admin_dashboard.html', pending_students=pending_students)

@app.route('/approve/<usn>')
def approve(usn):
    # Update student status to 'approved'
    db.collection('student').document(usn).update({'status': 'approved'})
    flash(f'Registration request for USN {usn} has been approved.')
    return redirect(url_for('admin_dashboard'))

"""if __name__ == '__main__':
    app.run(debug=True)"""
