from flask import Flask, request, jsonify
from flask_cors import CORS
import rpy2.robjects as robjects
import math
import rpy2.robjects.packages as rpackages
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import logging


app = Flask(__name__)
CORS(app)

# Load the R "base" package (required for certain date operations)
r_base = rpackages.importr('base')

@app.route('/submit', methods=['POST'])
def handle_submission():
    data = request.json
    name = f"{data['firstName']} {data['lastName']}"
    dob = data['dob']
    email = data['email']
    print(name, dob, email)

    # Define the R function for age and weekday calculation
    robjects.r('''
        calculate_age_and_weekday <- function(dob) {
            dob_date <- as.Date(dob)
            current_date <- Sys.Date()
            age <- as.numeric(difftime(current_date, dob_date, units = "weeks")) / 52.25
            weekday <- weekdays(dob_date)
            return(c(age, weekday))
        }
    ''')

    # Call the R function
    r_func = robjects.globalenv['calculate_age_and_weekday']
    age_weekday = r_func(dob)

    # Extract results from R code
    age = int(math.floor(float(age_weekday[0])))
    weekday = age_weekday[1][0]

    print(f"Age: {age}, Day of Week: {weekday}")

    # PDF Generation
    pdf_filename = f"{data['firstName']}_{data['lastName']}_info.pdf"
    c = canvas.Canvas(pdf_filename)
    c.drawString(100, 750, f"Name: {name}")
    c.drawString(100, 730, f"Age: {age}")
    c.drawString(100, 710, f"Day of the Week of Birth: {weekday}")
    c.save()

    # Email Sending
    sender_email = os.environ.get('DEMO_EMAIL')
    sender_password = os.environ.get('DEMO_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Your Details"

    with open(pdf_filename, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(pdf_filename))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_filename)}"'
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        logging.info("Email sent successfully")
        return jsonify({"message": "Email sent successfully"})
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
