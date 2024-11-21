import csv
from email.message import EmailMessage
import smtplib


def get_credentials(filepath):
    with open("credentials.txt", "r") as f:
        email_address = f.readline()
        email_pass = f.readline()
    return (email_address, email_pass)


def login(email_address, email_pass, s):
    s.ehlo()
    # start TLS for security
    s.starttls()
    s.ehlo()
    # Authentication
    s.login(email_address, email_pass)
    print("login")


def send_mail():
    s = smtplib.SMTP("smtp.gmail.com", 587)
    email_address, email_pass = get_credentials("./credentials.txt")
    login(email_address, email_pass, s)

    # message to be sent
    subject = "Explore Vietnam"
    body = """Vietnam is a country located in Southeast Asia,
    known for its diverse landscapes and rich culture.\n
    Vietnam is also famous for its unique cuisine,
    from pho and banh mi to regional specialties.\n
    The country's folk culture, traditional festivals"""

    message = EmailMessage()
    message.set_content(body)
    message['Subject'] = subject

    with open("emails.csv", newline="") as csvfile:
        spamreader = csv.reader(csvfile, delimiter=" ", quotechar="|")
        for email in spamreader:
            s.send_message(email_address, email[0], message)
            print("Send To " + email[0])

    # terminating the session
    s.quit()
    print("sent")


if __name__ == "__main__":
    send_mail()

#source code >> Quang-Ng-Duong