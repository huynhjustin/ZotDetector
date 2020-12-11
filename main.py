# Import packages
from flask import Flask, render_template, Response, request, url_for, redirect
from camera import VideoCamera
import requests

# Initialize Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Render webpage
    return render_template('index.html', content="Dylan") #replace Dylan with Name

@app.route('/statistics/')
def statistics():
    return render_template('statistics.html') 
# EOF #

def generate(camera):
    while True:
        # Get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
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

if __name__ == '__main__':
    # Set server address and port (localhost:5000)
    app.run(host='0.0.0.0',port='5000', debug=True)