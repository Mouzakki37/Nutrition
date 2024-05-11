from django .core.mail import send_mail
from django.conf import settings

from smtplib import SMTPException


def send_fgt_pssw_mail(email,token):
    
    subject ='Password Link'
    message = f'Click on the link to change your password http://127.0.0.1:8000/change_passw/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
   
    try:
       send_mail(subject, message, email_from, recipient_list)  
    except SMTPException as e:
     print("SMTP Error:", e)
    
    
    # send_mail(subject, message, email_from, recipient_list)
    return True
    
    
    
