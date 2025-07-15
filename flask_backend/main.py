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
import uuid
from flask_cors import CORS
from datetime import datetime

load_dotenv()
EMAIL_APP_PASSWORD = os.getenv("EMAIL_PASSWORD") 

# Get Supabase URL and Service Role Key from the environment
SUPABASE_URL = os.getenv("VITE_SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Check if the environment variables are loaded correctly
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Supabase URL or Service Role Key not found in environment variables.")

# Create the Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
camera = cv2.VideoCapture(0)  # Webcam
detector = cv2.QRCodeDetector()
qr_data = ""
current_attendance_status_message = "Waiting for QR code..."
processed_qr_values_session = set() # For immediate in-session deduplication


#opencv camera
# def generate_frames():
#     global qr_data
#     while True:
#         success, frame = camera.read()
#         if not success:
#             break

#         # QR code detection
#         data, _, _ = detector.detectAndDecode(frame)
#         if data:
#             qr_data = data
#             print("QR Code:", data)

#         # Encode frame as JPEG
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         # Stream to client
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames():
    global qr_data
    while True:
        success, frame = camera.read()
        if not success:
            break

        # QR code detection
        data, _, _ = detector.detectAndDecode(frame)
        if data:
            scanned_qr_value = data.strip()
            qr_data = scanned_qr_value  # Store the current QR value for use by frontend

            if scanned_qr_value in processed_qr_values_session:
                current_attendance_status_message = f"QR Code {scanned_qr_value} already processed recently."
            else:
                try:
                    # Step 1: Check for existing record in Supabase
                    existing_record_response = supabase.table('Event_attendees') \
                        .select('user_email, name, event_id, status') \
                        .eq('qr_code_value', scanned_qr_value) \
                        .limit(1) \
                        .execute()

                    if existing_record_response.data:
                        record = existing_record_response.data[0]
                        attendee_email = record.get('user_email')
                        attendee_name = record.get('name')
                        event_id = record.get('event_id')
                        status = record.get('status')

                        if status != "Checked In":
                            # Step 2: Update status to 'Checked In'
                            update_response = supabase.table('Event_attendees') \
                                .update({
                                    'status': 'Checked In',
                                }) \
                                .eq('user_email', attendee_email) \
                                .execute()

                            if update_response.data:
                                print(f"Checked in: {attendee_name} ({attendee_email}) for event {event_id}")
                                current_attendance_status_message = f"✅ {attendee_name} checked in!"
                            else:
                                print(f"Update failed for {scanned_qr_value}: {update_response}")
                                current_attendance_status_message = "❌ Error updating attendance."

                        else:
                            print(f"{attendee_name} already checked in.")
                            current_attendance_status_message = f"⚠️ {attendee_name} already checked in."

                        processed_qr_values_session.add(scanned_qr_value)

                    else:
                        print(f"QR not found in Event_attendees: {scanned_qr_value}")
                        current_attendance_status_message = "❌ QR not found or not registered."
                        processed_qr_values_session.add(scanned_qr_value)

                except Exception as e:
                    print(f"Error checking in QR: {e}")
                    current_attendance_status_message = "❌ Backend error during check-in."

            # Reset qr_data after processing this QR code
            qr_data = None  # Reset qr_data to None after processing

        # Encode frame as JPEG for streaming
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

@app.route("/send_email_reminder", methods=["POST"])

def send_email_reminder():
    data = request.get_json()
    recipient = data.get("recipient")
    event_name = data.get("eventName")

    subject = f"Reminder: Upcoming Event - {event_name}"
    message_body = f"""Hello,

This is a friendly reminder about the upcoming event: **{event_name}**.

Make sure to check your schedule and prepare accordingly. We’re excited to see you there!

Best regards,  
Your Community Team"""

    try:
        email_address = "collectivedeeptech@gmail.com"
        email_password = EMAIL_APP_PASSWORD

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email_address
        msg['To'] =  recipient
        msg.set_content(message_body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            smtp.send_message(msg)

        return jsonify({"status": "success", "message": "Email reminder sent!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/send_email_python", methods=["POST"])
def send_email_python():
    data = request.get_json()
    attendee_name = data.get("attendeeName")
    attendee_email = data.get("attendeeEmail")
    event_name = data.get("eventName")
    event_date = data.get("eventDate")
    event_location = data.get("eventLocation")

    if not all([attendee_name, attendee_email, event_name, event_date, event_location]):
        return jsonify({"status": "error", "message": "Missing required data for QR ticket generation."}), 400

    try:
        # Step 1: Check/Create Registration in 'Event_attendees' Table based on user_email
        existing_registration_response = supabase.table('Event_attendees') \
            .select('user_email, qr_code_value') \
            .eq('user_email', attendee_email) \
            .eq('event_id', event_name) \
            .limit(1) \
            .execute()

        if existing_registration_response.data:
            record = existing_registration_response.data[0]
            existing_qr_value = record.get('qr_code_value')

            if existing_qr_value:
                qr_value_to_encode = existing_qr_value
            else:
                qr_value_to_encode = str(uuid.uuid4())  # Generate new QR if none exists
                # Update the record with the new QR code
                update_response = supabase.table('Event_attendees') \
                    .update({'qr_code_value': qr_value_to_encode}) \
                    .eq('user_email', attendee_email) \
                    .eq('event_id', event_name) \
                    .execute()

                if not update_response.data:
                    return jsonify({"status": "error", "message": "Failed to update existing registration with QR code."}), 500
        else:
            # If no record exists, create a new registration with user_email
            qr_value_to_encode = str(uuid.uuid4())  # Generate new QR code
            insert_response = supabase.table('Event_attendees').insert({
                "user_email": attendee_email,
                "event_id": event_name,  # Assuming event_name can be used as an event identifier
                "qr_code_value": qr_value_to_encode,
                "name": attendee_name,
                "status": 'Registered'
            }).execute()

            if not insert_response.data:
                return jsonify({"status": "error", "message": "Failed to register attendee for event."}), 500

        # Step 2: Generate the QR code image
        qr_img = qrcode.make(qr_value_to_encode)
        img_byte_arr = BytesIO()
        qr_img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # Step 3: Create the PDF with the QR code
        pdf_buffer = BytesIO()
        width, height = landscape(A4)
        c = canvas.Canvas(pdf_buffer, pagesize=(width, height))

        c.setStrokeColor(colors.darkblue)
        c.setLineWidth(2)
        c.rect(10 * mm, 10 * mm, width - 20 * mm, height - 20 * mm)

        c.setFont("Helvetica-Bold", 20)
        c.drawString(20 * mm, height - 25 * mm, f"🎟 {event_name}")

        c.setFont("Helvetica", 12)
        c.drawString(20 * mm, height - 35 * mm, f"Name: {attendee_name}")
        c.drawString(20 * mm, height - 45 * mm, f"Email: {attendee_email}")
        c.drawString(20 * mm, height - 55 * mm, f"Date: {event_date}")
        c.drawString(20 * mm, height - 65 * mm, f"Location: {event_location}")

        c.setStrokeColor(colors.grey)
        c.line(width / 2, 20 * mm, width / 2, height - 20 * mm)

        qr_reader = ImageReader(img_byte_arr)
        qr_size = 200
        qr_x = width - 30 * mm - qr_size
        qr_y = height / 2
        c.drawImage(qr_reader, qr_x, qr_y, width=qr_size, height=qr_size)

        c.setFont("Helvetica", 8)
        c.setFillColor(colors.grey)
        c.drawCentredString(qr_x + qr_size / 2, qr_y - 10, "Scan to check in")

        c.showPage()
        c.save()
        pdf_buffer.seek(0)

        # Step 4: Create and send email
        msg = EmailMessage()
        msg['Subject'] = f"Your Digital QR Code Pass for {event_name}"
        msg['From'] = "collectivedeeptech@gmail.com"
        msg['To'] = attendee_email
        msg.set_content(f"Hello {attendee_name},\n\nHere is your QR code for the event '{event_name}'.")

        msg.add_attachment(pdf_buffer.read(), maintype="application", subtype="pdf", filename="qr_ticket.pdf")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('collectivedeeptech@gmail.com', EMAIL_APP_PASSWORD)  # App password only
            smtp.send_message(msg)

        return jsonify({"status": "success", "message": "Email with QR code sent successfully!"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500



# Run the app
if __name__ == '__main__':
    app.run(debug=True)
