from flask import Flask, render_template, Response, request, jsonify
import serial
import time

app = Flask(__name__)

# Replace with your Arduino serial port and baud rate
arduino_serial = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Give time for Arduino to reset

# Route for rendering the HTML UI
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling camera feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to send control commands to the Arduino
@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    command_type = data.get('type')

    if command_type == 'movement':
        angle = data.get('angle', None)
        force = data.get('force', None)
        command = data.get('command', None)
        
        if command == 'stop':
            send_to_arduino('M0')  # Stop the rover
        else:
            send_movement_command(angle, force)

    elif command_type == 'camera':
        angle = data.get('angle', None)
        force = data.get('force', None)
        command = data.get('command', None)
        
        if command == 'stop':
            send_to_arduino('C0')  # Stop the camera
        else:
            send_camera_command(angle, force)

    elif command_type == 'headlights':
        state = data.get('state', False)
        if state:
            send_to_arduino('H1')  # Turn on headlights
        else:
            send_to_arduino('H0')  # Turn off headlights

    elif command_type == 'buzzer':
        state = data.get('state', False)
        if state:
            send_to_arduino('B1')  # Turn on buzzer
        else:
            send_to_arduino('B0')  # Turn off buzzer

    return jsonify({'status': 'success'}), 200

# Helper functions
def send_to_arduino(message):
    arduino_serial.write(f"{message}\n".encode())

def send_movement_command(angle, force):
    # Translate the angle and force to a motor control command (custom logic)
    if 0 <= angle < 45 or 315 <= angle <= 360:
        send_to_arduino(f'MF{force}')  # Move forward
    elif 45 <= angle < 135:
        send_to_arduino(f'MR{force}')  # Move right
    elif 135 <= angle < 225:
        send_to_arduino(f'MB{force}')  # Move backward
    elif 225 <= angle < 315:
        send_to_arduino(f'ML{force}')  # Move left

def send_camera_command(angle, force):
    # Custom logic for camera control using the joystick
    if 0 <= angle < 45 or 315 <= angle <= 360:
        send_to_arduino(f'CUP{force}')  # Move camera up
    elif 45 <= angle < 135:
        send_to_arduino(f'CRIGHT{force}')  # Move camera right
    elif 135 <= angle < 225:
        send_to_arduino(f'CDOWN{force}')  # Move camera down
    elif 225 <= angle < 315:
        send_to_arduino(f'CLEFT{force}')  # Move camera left

# Camera feed generation (assuming PiCamera)
def gen_camera_feed():
    # Placeholder for PiCamera streaming code
    while True:
        frame = get_frame_from_camera()  # Get frame from the PiCamera
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def get_frame_from_camera():
    # Placeholder function for PiCamera frame capture
    return b''  # Empty byte string as placeholder

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
