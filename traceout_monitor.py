#!/usr/bin/env python

# https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postfix-as-a-send-only-smtp-server-on-ubuntu-14-04


import re
import subprocess
import smtplib
from email.mime.text import MIMEText

def is_running(process):
    s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE) 
    for x in s.stdout:
        if re.search(process, x):
            return True
    return False

def send_alert():
    sender = 'from@example.com'
    receivers = ['to@example.net']
    message = MIMEText("From: Prod app server")  
    message['Subject'] = "System Failure Alert"
    message['From'] = "from@example.com"
    message['To'] = "to@example.com"

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print "Successfully sent email"
    except IOError:
        print "Error: unable to send email"


def main():
    print send_alert()
    status = is_running('monitor') # monitoring monitor
    print status


if __name__ == '__main__':
    main()

