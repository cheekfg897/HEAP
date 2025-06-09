import resend
from flask import Flask, render_template, request, jsonify, Response
import cv2
import os
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY") 

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Webcam
detector = cv2.QRCodeDetector()
qr_data = ""

#opencv camera
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

#load index.html
@app.route('/')
def index():
    return render_template('index.html')

#generate live feed on frontend
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#index.html fetching for qr data from backend (if any)
@app.route('/attendance_status')
def get_data():
    return jsonify({"data": qr_data})


#function that uses Resend to send email
@app.route("/send_email")
def send_email():
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["Enter Your email you signup a resend account with here"],
        "subject": "hello world",
        "html": "<strong>it works!</strong>",
    }

    r = resend.Emails.send(params)
    return jsonify(r)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
