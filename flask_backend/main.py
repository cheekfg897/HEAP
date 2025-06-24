from flask import Flask, render_template, request, jsonify, Response
import cv2
import os
from dotenv import load_dotenv
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
import base64
import smtplib
from email.message import EmailMessage
from supabase.client import create_client, Client
import json

load_dotenv()
EMAIL_APP_PASSWORD = os.getenv("EMAIL_PASSWORD") 
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")  # MUST be service role

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

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

@app.route('/invite')
def invite():
    response = supabase.auth.admin.invite_user_by_email(
    "enter ur email here",
    {"redirect_to": "http://localhost:5000/accept-invite"}
)
    print(response)
    return json.dumps({"message": "User invited"})

@app.route('/accept-invite')
def accept_invite():
    # Serve an HTML page with JS to handle tokens and call supabase.auth.setSession()
    return render_template('accept_invite.html')

#generate live feed on frontend
@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#index.html fetching for qr data from backend (if any)
@app.route('/attendance_status')
def get_data():
    return jsonify({"data": qr_data})

@app.route("/send_email_python")
def send_email_python():
    # Step 0: Generate the QR code
    qr_data = "https://www.example.com/your-exclusive-offer"
    qr_img = qrcode.make(qr_data)

    # Step 1: Save QR to a BytesIO stream (in-memory file)
    img_byte_arr = BytesIO()
    qr_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # Important: move to the beginning of the stream

    # Step 2: Create a blank PDF with only the QR code
    pdf_buffer = BytesIO()
    width, height = landscape(A4)
    c = canvas.Canvas(pdf_buffer, pagesize=(width, height))
    # === Ticket Border ===
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(2)
    c.rect(10 * mm, 10 * mm, width - 20 * mm, height - 20 * mm)

    # === Title ===
    c.setFont("Helvetica-Bold", 20)
    c.drawString(20 * mm, height - 25 * mm, "🎟 SMU HEAP 2025")

    # === Subtitle / Details ===
    c.setFont("Helvetica", 12)
    c.drawString(20 * mm, height - 35 * mm, "Name: Kevan Soon")
    c.drawString(20 * mm, height - 45 * mm, "Role: Mentee")
    c.drawString(20 * mm, height - 55 * mm, "Date: June 17, 2025")
    c.drawString(20 * mm, height - 65 * mm, "Location: Computing Lab 1")

    # === Divider Line ===
    c.setStrokeColor(colors.grey)
    c.line(width / 2, 20 * mm, width / 2, height - 20 * mm)

    # === QR Code on the right side ===
    qr_reader = ImageReader(img_byte_arr)
    qr_size = 200  # in points (~mm)
    qr_x = width - 30 * mm - qr_size
    qr_y = height / 2 
    c.drawImage(qr_reader, qr_x, qr_y, width=qr_size, height=qr_size)


    # === QR Text Label ===
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 10, "Scan to check in")

    c.showPage()
    c.save()
    pdf_buffer.seek(0)

    # Step 3: Create email
    msg = EmailMessage()
    msg['Subject'] = "Your Digital QR Code Pass"
    msg['From'] = "kevansoon@gmail.com"
    msg['To'] = "kevan.soon.2024@smu.edu.sg"
    msg.set_content("Here is your QR code attached as an image!")

    msg.add_attachment(pdf_buffer.read(), maintype="application", subtype="pdf", filename="qr_ticket.pdf")



    # Optional: Embed inline image (HTML email)
    # msg.add_alternative(f"""
    # <html>
    # <body>
    #     <p>Hi there!</p>
    #     <p>Scan your QR code below:</p>
    #     <img src="cid:qrimage">
    # </body>
    # </html>
    # """, subtype='html')
    # Step 4: Add QR code image as attachment (both inline and file)
    # msg.get_payload()[1].add_related(img_byte_arr.read(), 'image', 'png', cid='qrimage')
    # Reset stream again if you want to also attach as downloadable
    # img_byte_arr.seek(0)
    # msg.add_attachment(img_byte_arr.read(), maintype='image', subtype='png', filename='qr_code.png')
    # Attach PDF
    
    # Step 5: Send email using Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('kevansoon@gmail.com', EMAIL_APP_PASSWORD)  # App password only
        smtp.send_message(msg)
    
    print("email sent successfully")


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
