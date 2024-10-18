from flask import Flask, render_template, Response, request, jsonify
import serial
import time
import cv2

app = Flask(__name__)

# Replace with your Arduino port
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)

# Function to send commands to Arduino
def send_command_to_arduino(command):
    try:
        arduino.write(command.encode())
    except Exception as e:
        print(f"Error sending command to Arduino: {e}")

# Route for the index page
@app.route('/')
def index():
    return render_template('rover_new.html')

# Route to control the rover via POST request
@app.route('/control', methods=['POST'])
def control():
    data = request.json
    command = data.get('command')

    if command:
        send_command_to_arduino(command)
        return jsonify({'status': 'success', 'command': command})
    else:
        return jsonify({'status': 'error', 'message': 'No command received'})

# Route for video feed
def gen():
    camera = cv2.VideoCapture(0)  # Replace with Pi Camera source
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
