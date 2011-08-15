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
    return Popen(cmdline.split()).wait()

def email(from_addr, to, subject, server, pw='', body=None, attachment_pdf=None):
    """Send an email through the gmail account
    http://stackoverflow.com/questions/778202/smtplib-and-gmail-python-script-problems
    """
    #create a message
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to
    msg['Subject'] = subject
    msg.preamble = 'Multipart message.\n'
    
    # attach body text
    if body:
        part = MIMEText(body)
        msg.attach(part)

    if attachment_pdf and os.path.isfile(attachment_pdf):
        #open and attach the pdf
        part = MIMEApplication(open(attachment_pdf, 'rb').read())
        bname = os.path.basename(attachment_pdf)
        part.add_header('Content-Disposition', 'attachment', filename=bname)
        msg.attach(part)
    
    #message is finished

    #start, connect, and if need be, authorize server
    if server == 'smtp.gmail.com':
        smtp = smtplib. SMTP(server, 587)
        smtp.starttls()
        smtp.login(from_addr, pw)
    else:
        smtp = smtplib.SMTP(server)
    
    #sendmail
    resp = smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    
    if resp:
        print("Something happened to your email...")
    smtp.quit()
    
