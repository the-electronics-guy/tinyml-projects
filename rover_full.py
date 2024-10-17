from flask import Flask, render_template, request, jsonify, Response
import serial
import cv2

app = Flask(__name__)

# Initialize serial communication with Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust this to match your setup

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control_rover():
    data = request.json
    command = data['command']
    print(f"Received command: {command}")

    # Send command to Arduino via serial
    if command in ['forward', 'backward', 'left', 'right', 'stop', 'headlights', 'buzzer']:
        ser.write(command.encode())

    return jsonify({"status": "success", "command": command})

def gen_video_feed():
    camera = cv2.VideoCapture(0)  # Use your Pi camera or other camera source
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__
