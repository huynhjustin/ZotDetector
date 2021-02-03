# Import packages
from flask import Flask, render_template, Response, request, url_for, redirect
from camera import VideoCamera
import requests
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

button_flag = False

# Connect to local mySQL database and extract table
connection = mysql.connector.connect(user='root', password='password', database='zotdetectordb')
cursor = connection.cursor()
cursor.execute("SELECT * FROM student") # Run this query
#rows = cursor.fetchall()
sql_data = "<table style='border:1px solid red'>"
sql_data_raw = []
for row in cursor:
    sql_data = sql_data + "<tr>"
    for i in row:
        sql_data = sql_data + "<td>" + str(i) + "</td>"
        sql_data_raw.append(i)
    sql_data = sql_data + "</tr>"
connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Render webpage
    return render_template('index.html', content="Dylan", sql_data=sql_data_raw) #replace Dylan with Name

@app.route('/statistics/')
def statistics():
    return render_template('statistics.html') 
# EOF #

def generate(camera):
    while button_flag:
        # Get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    emotions_sum = sum(camera.emotions_count.values())
    print(emotions_sum)
    if emotions_sum > 0:
        for i in camera.emotions_count:
            camera.emotions_count[i] = (camera.emotions_count[i]*100.0)/emotions_sum
        print(camera.emotions_count)
    # Put it into the database here
# EOF #

# Video feed for HTML
@app.route('/video_feed')
def video_feed():
    return Response(generate(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
# EOF #

@app.route('/hello')
def hello():
    # api-endpoint 
    URL = "http://localhost:8080/api/ret/student?id=476"
    
    # defining a params dict for the parameters to be sent to the API 
    #PARAMS = {'address':location} 
    
    # sending get request and saving the response as response object 
    r = requests.get(url = URL) 
    
    # extracting data in json format 
    data = r.json() 
    print(data)
    return r.content

@app.route('/disclaimer', methods=['GET', 'POST'])
def disclaimer():
    if request.method == 'POST':
        if request.form['submit_button'] == 'OK':
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("disclaimer.html")

@app.route('/sqltest') # At this address, display table from mySQL query
def sqltest():
    return "<html><body>" + sql_data + "</body></html>" # Return with HTML tags

@app.route('/your_flask_function')
def change_button_flag():
    global button_flag
    button_flag = not button_flag
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Set server address and port (localhost:5000)
    app.run(host='0.0.0.0',port='5000', debug=True)