# Import packages
from flask import Flask, render_template, Response
from camera import VideoCamera

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Render webpage
    return render_template('index.html')
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

if __name__ == '__main__':
    # Set server address and port (localhost:5000)
    app.run(host='0.0.0.0',port='5000', debug=True)