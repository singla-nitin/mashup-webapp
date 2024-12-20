from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
CORS(app)  

UPLOAD_DIR = "outputs"

# Ensure output directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route("/create_mashup", methods=["POST"])
def create_mashup():
    data = request.get_json()
    singer = data["singer"]
    videos = data["videos"]
    duration = data["duration"]
    email = data["email"]

    # Output filename
    output_file = f"{UPLOAD_DIR}/mashup_output.mp3"

    try:
       
        subprocess.run(
            ["python", "102203984.py", singer, videos, duration, output_file],
            check=True,
        )

      
        zip_filename = f"{UPLOAD_DIR}/mashup.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            zipf.write(output_file, arcname="mashup_output.mp3")

        
        send_email(email, zip_filename)

        return jsonify({"message": "Mashup created and sent to your email!"})

    except Exception as e:
        print(e)
        return jsonify({"message": "Error creating mashup"}), 500

def send_email(to_email, zip_filepath):
    sender_email = "nitinsingla703@gmail.com"
    sender_password = "nitin@2003"

    # Email setup
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = "Your Mashup File"

    # Attach the ZIP file
    with open(zip_filepath, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=mashup.zip")
        msg.attach(part)

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())

if __name__ == "__main__":
    app.run(debug=True)
