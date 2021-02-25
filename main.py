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
id = 837 # Default ID number

url = "http://localhost:8080/api/ret/student?id={id}".format(id=id)
user_info = requests.get(url = url).json()["student"]
name = user_info['firstName']

# Connect to local mySQL database and extract table
connection = mysql.connector.connect(user='root', password='password', database='zotdetectordb')
cursor = connection.cursor()
cursor.execute("SELECT * FROM student") # Run this query
#rows = cursor.fetchall()
sql_data = "<table style='border:1px solid red'>"
sql_data = sql_data + "<tr><td>ID</td><td>Email</td><td>First Name</td><td>Last Name</td></tr>"
sql_data_raw = []
for row in cursor:
    sql_data = sql_data + "<tr>"
    for i in row:
        sql_data = sql_data + "<td>" + str(i) + "</td>"
        sql_data_raw.append(i)
    sql_data = sql_data + "</tr>"

print(sql_data)
connection.close()

# Emotions for current week for HTML
def retrieve_weekly_emotions():
    # Resulting emotions array used for summary
    emotions_results = dict()
    # List of days as Strings and default emotions
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    default_emotions = {"angry": 0, "disgusted": 0, "fearful": 0, "happy": 0, "neutral": 0, "sad": 0, "surprised": 0}
    # GET request API URL for retrieving emotions
    # TODO: Make dynamic to get id of student requesting
    #id = 845
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
    # Retrieve data for weekly chart
    start, end, emotions = retrieve_weekly_emotions()
    # Render webpage
    return render_template('index.html', name=name, start_date=start, end_date=end, emotions_data=emotions, sql_data=sql_data_raw, button=button_text)

def generate(camera):
    while button_flag:
        # Get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    emotions_sum = sum(camera.emotions_count.values())
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
# EOF #

# Video feed for HTML
@app.route('/video_feed')
def video_feed():
    return Response(generate(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# EOF #

@app.route('/disclaimer', methods=['GET', 'POST'])
def disclaimer():
    if request.method == 'POST':
        if request.form['submit_button'] == 'OK':
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("disclaimer.html")

@app.route('/registered')
def registered():    
    return "<html><body>" + sql_data + "</body></html>"

@app.route('/record-button', methods=['GET', 'POST'])
def change_button_flag():
    global button_flag
    global button_text
    global id
    global name
    button_flag = not button_flag
    if button_text == "Start Recording":
        button_text = "Stop Recording"
    else:
        button_text = "Start Recording"
    
    # ID change
    id_form = request.form['id'] # Retrieve ID from form on frontend
    if len(id_form) > 0 and id_form.isdigit():  # If a value was entered and it was a number, set the id value to this value
        id = int(id_form)
        url = "http://localhost:8080/api/ret/student?id={id}".format(id=id)
        user_info = requests.get(url = url).json()["student"]
        name = user_info['firstName']
    return redirect(url_for('index'))

@app.route('/register-user', methods=['GET', 'POST'])
def register():
    name = request.form['name']
    email = request.form['email']

    # Put user into database
    url = 'http://localhost:8080/api/data/student' # Define API url
    headers = {'Content-Type': 'application/json'} # Define headers for input type
    data_json = json.dumps({"name": name, "email": email}) # Create body for POST request

    x = requests.request("POST", url, headers=headers, data=data_json) # POST Request to input into database
    print(x.text) # Print response

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Set server address and port (localhost:5000)
    app.run(host='0.0.0.0',port='5000', debug=True)