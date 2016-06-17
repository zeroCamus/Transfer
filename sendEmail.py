import smtplib
from email.mime.text import MIMEText
'''
def sendme(title, text):
	title is the subject of your e-mail.
	text is the value of your e-mail.
	适用于Python3
'''
def sendme(title, text):
    msg = MIMEText(text)
    msg['Subject'] = title
    msg['From'] = "huohuliu@126.com"
    msg['To'] = "fly199701@126.com"
    s = smtplib.SMTP('smtp.126.com')
    s.login('huohuliu', 'huohuxxttvv')
    s.send_message(msg)
    s.quit()

if __name__ == '__main__':
    sendme("Hello World", "Welcome")
