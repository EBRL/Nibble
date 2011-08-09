#!/usr/bin/env python

"""
Copyright (c) 2011, Scott Burns
All rights reserved.
"""
from subprocess import Popen

from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

import os

def run_cmdline(cmdline):
    """ Start a process"""
    print("Starting %s" % cmdline)
    p = Popen(cmdline.split())
    return p.wait()

def email(to, subject, body=None, attachment_pdf=None):
    """Send an email through the gmail account"""
    #create a message
    msg = MIMEMultipart()
    msg['From'] = "ebrl.nibble@gmail.com"
    msg['To'] = to
    msg['Subject'] = subject
    msg.preamble = 'Multipart message.\n'
    
    # attach body text
    if body:
        part = MIMEText(body)
        msg.attach(part)

    if attachment_pdf:
        #open and attach the pdf
        part = MIMEApplication(open(attachment_pdf, 'rb').read())
        bname = os.path.basename(attachment_pdf)
        part.add_header('Content-Disposition', 'attachment', filename=bname)
        msg.attach(part)
    
    #message is finished

    #start, connect, and authorize smtp.gmail.com
    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.starttls()
    gmail.login('ebrl.nibble', 'HEC004!!')
    
    #sendmail
    resp = gmail.sendmail(msg['From'], msg['To'], msg.as_string())
    
    if resp:
        print("Something happened to your email...")
    gmail.quit()
    
