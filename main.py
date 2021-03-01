# Import packages
from flask import Flask, render_template, Response, request, url_for, redirect
from camera import VideoCamera
from datetime import datetime, timedelta, date
import calendar
import requests
import mysql.connector
import json

# Initialize Flask app
app = Flask(__name__)

button_flag = False
button_text = "Start Recording"
id = None
logged_in = False

# Emotions for current week for HTML
def retrieve_weekly_emotions():
    # Resulting emotions array used for summary
    emotions_results = dict()
    # List of days as Strings and default emotions
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    default_emotions = {"angry": 0, "disgusted": 0, "fearful": 0, "happy": 0, "neutral": 0, "sad": 0, "surprised": 0}
    # GET request API URL for retrieving emotions
    today = datetime.now()
    start = today - timedelta(today.weekday())
    end = start + timedelta(6)
    duration = (today-start).days
    url = "http://localhost:8080/api/ret/all_emotions?id={id}&duration={duration}".format(id=id, duration=duration)
    # Emotion data json
    emotions = requests.get(url = url).json()["emotions"]
    for emotion in emotions:
        date = datetime.strptime(emotion["date"], '%Y-%m-%d')
        day = calendar.day_name[datetime.combine(date, datetime.min.time()).weekday()]
        emotions_results[day] = emotion["emotions"]
    # Fill in missing days will zero values
    for day in days_of_week:
        if day not in emotions_results: emotions_results[day] = default_emotions
    return (start.date().strftime("%B %d, %Y"), end.date().strftime("%B %d, %Y"), emotions_results)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if user already logged in
    if logged_in:
        # Retrieve data for weekly chart
        start, end, emotions = retrieve_weekly_emotions()
        # Render webpage
        return render_template('index.html', name=name, start_date=start, end_date=end, emotions_data=emotions, button=button_text)
    # If not logged in then redirect to login page
    else: return render_template('login.html')

def generate(camera):
    while button_flag:
        # Get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    emotions_sum = sum(camera.emotions_count.values())
    print(camera.emotions_count.values())
    if emotions_sum > 0:
        # Put it into the database here
        url = 'http://localhost:8080/api/data/emotion' # Define API url
        headers = {'Content-Type': 'application/json'} # Define headers for input type
        emotions_dict = json.dumps(camera.emotions_count) # Create JSON string from emotions dictionary
        emotions_dict_loaded = json.loads(emotions_dict)  # Load dictionary
        today = datetime.now().strftime('%Y-%m-%d') # Get current day
        data_json = json.dumps({"id": id, "date": today, "emotions": emotions_dict_loaded}) # Create body for POST request
        x = requests.request("POST", url, headers=headers, data=data_json) # POST Request to input into database
        print(x.text) # Print response

# Video feed for HTML
@app.route('/video_feed')
def video_feed():
    return Response(generate(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/record-button', methods=['GET', 'POST'])
def change_button_flag():
    global button_flag
    global button_text
    button_flag = not button_flag

    # Change text for start/stop recording button
    if button_text == "Start Recording": button_text = "Stop Recording"
    else: button_text = "Start Recording"
    return redirect(url_for('index'))

# Disclaimer route for HTML
@app.route('/disclaimer', methods=['GET', 'POST'])
def disclaimer():
    if request.method == 'POST':
        if request.form['submit_button'] == 'OK':
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("disclaimer.html")

# How to Use route for HTML
@app.route('/how_to', methods=['GET', 'POST'])
def how_to():
    if request.method == 'POST':
        if request.form['submit_button'] == 'OK':
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("howto.html")

# Register new user for HTML
@app.route('/register', methods=['GET', 'POST'])
def register():
    global id
    global name
    global logged_in
    error = None

    if request.method == "POST":
        # Get Student information
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']

        # Put user into database
        url = 'http://localhost:8080/api/data/student' # Define API url
        headers = {'Content-Type': 'application/json'} # Define headers for input type
        data_json = json.dumps({"name": first_name + " " + last_name, "email": email})   # Create body for POST request
        response = requests.request("POST", url, headers=headers, data=data_json).json() # POST Request to input into database
        # Verify if any errors
        if (response["success"]):
            id = response["id"]
            name = first_name
            logged_in = True
            print(id)
            return redirect(url_for('index'))
        else: error = response["message"]
    return render_template('register.html', error=error)

# Login for HTML
@app.route('/login', methods=['GET','POST'])
def login():
    global id
    global name
    global logged_in
    error = None

    if request.method == "POST":
        # Get Student record with email
        email = request.form.get('email','')
        url = 'http://localhost:8080/api/ret/student?email={email}'.format(email=email)
        response = requests.get(url = url).json()
        print(response)
        # Verify if Student record exists
        if (response["success"] and response["student"]["id"] != -1):
            id = response["student"]["id"]
            name = response["student"]["firstName"]
            logged_in = True
            return redirect(url_for('index'))
        else: error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

# Logout for HTML
@app.route("/logout")
def logout():
    global logged_in
    logged_in = False
    return index()

if __name__ == '__main__':
    # Set server address and port (localhost:5000)
    app.run(host='0.0.0.0',port='5000', debug=True)