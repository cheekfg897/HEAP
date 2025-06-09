from flask import Flask, render_template, request, jsonify, Response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Webcam
detector = cv2.QRCodeDetector()
qr_data = ""

def generate_frames():
    global qr_data
    while True:
        success, frame = camera.read()
        if not success:
            break

        # QR code detection
        data, _, _ = detector.detectAndDecode(frame)
        if data:
            qr_data = data
            print("QR Code:", data)

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Stream to client
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Home route
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/attendance_status')
def get_data():
    return jsonify({"data": qr_data})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
