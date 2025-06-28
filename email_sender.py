import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config import config

def send_application(job_info, cv_text, cover_letter):
    """Send application via email with self-healing features"""
    # TODO: In a real system, we would extract the hiring manager's email from job_info. 
    # For now, we use a placeholder or skip if not available.
    if 'email' not in job_info:
        print(f"No email found for {job_info['title']} at {job_info['company']}. Skipping.")
        return False

    msg = MIMEMultipart()
    msg['Subject'] = f"Application for {job_info['title']} Position"
    msg['From'] = config.EMAIL_USER
    msg['To'] = job_info['email']  # This should be set from job_info

    # Add body
    msg.attach(MIMEText(cover_letter, 'plain'))
    
    # Add CV attachment
    cv_attachment = MIMEApplication(cv_text.encode('utf-8'), Name="custom_cv.txt")
    cv_attachment['Content-Disposition'] = f'attachment; filename="custom_cv.txt"'
    msg.attach(cv_attachment)
    
    # Self-healing email send with retries
    for attempt in range(config.EMAIL_RETRY_LIMIT):
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(config.EMAIL_USER, config.EMAIL_PASS)
                server.send_message(msg)
            print(f"Application sent for {job_info['title']}")
            return True
        except Exception as e:
            print(f"Email error (attempt {attempt+1}): {str(e)}")
            time.sleep(5)
    return False
