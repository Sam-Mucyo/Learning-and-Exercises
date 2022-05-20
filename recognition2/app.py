from cs50 import SQL
import face_recognition
import pickle
from flask import Flask, flash, redirect, render_template, request, session, Response, jsonify
from flask_session import Session
from myfunctions import VideoCamera, known_people, who_is_this, apology
from cs50 import SQL
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import cv2


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///attendance.db")

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

global new_face_id, attendance, registering, is_known
attendance = False
registering = False
is_known = False

@app.route('/')
def index():
    return render_template('index.html')


# ---------- Registering a person -------

@app.route("/register", methods=["GET", "POST"])
def register():
    global new_face_id, attendance, registering, is_known
    attendance=False
    registering=True
    """Register user"""
    if request.method == "POST":

        name = request.form.get("name");
        contact = request.form.get("contact")

        # Ensure username is not blank
        if not name:
            return apology("Please put in the username", 400)

        # Ensure username is not blank
        if not contact:
            return apology("Please input your phone number", 400) 
        
        # Ensure contact has number type
        if not contact.isdigit() or int(contact) < 0 :
            return apology("Check contact format: No parenthesis or dashes", 400)
        
        # Ensure a Face was detected. b'\x80\x04]\x94.' represents an empty BLOB data
        if new_face_id == b'\x80\x04]\x94.':
            return apology("Sorry, No Face was detected ", 400)

        # Ensure the Face is not already in database
        if is_known:
            is_known = False
            return apology ("Sorry, it seems like the person already exists in database")


        # Query database for username
        rows = db.execute("SELECT * FROM people WHERE name = ?", name)

        # Ensure username is not already in the database 
        if len(rows) > 0:
            return apology("The username is already taken", 400)

        db.execute("INSERT INTO people (name, contact, face_id) VALUES (?, ?, ?)", name, contact, new_face_id)

        flash("Registration done successfully!")
        return redirect("/")

    else:
        return render_template("register.html")


def update_face_id(frame):
    global new_face_id, attendance, registering, is_known

    # Get the facial encodings of the user   
    img = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(img)
    encodesCurFrame = face_recognition.face_encodings(img, facesCurFrame)
    print(f"In registration, encoded current face is {encodesCurFrame}")
        
    # Blob the facial encodings to be saved in the database as BLOB
    new_face_id = pickle.dumps(list(encodesCurFrame))

    # Check if the face is not already in database
    ids, facial_encodings = known_people()
    
    # For every Frame
    for target_face, faceLoc in zip(encodesCurFrame, facesCurFrame):
        # Keep checking if the person is known
        known, id, name = who_is_this(ids, facial_encodings, target_face) 
        is_known = known

# ---------- Attendance -------

@app.route("/attendance", methods=["GET", "POST"])
def test():
    global new_face_id, attendance, registering
    attendance=True
    registering=False

    return render_template('test1.html')

             
@app.route('/video_feed')
def video_feed():
    video_stream = VideoCamera()
    return Response(generate_frame(video_stream),
            mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frame(camera):
    while True:
        frame = camera.get_frame()        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
