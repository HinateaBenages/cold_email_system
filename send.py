import csv
import smtplib
import os
import time
import random
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime, timedelta

TEST_MODE = False

# Charger variables .env
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Connexion Gmail SMTP
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL_USER, EMAIL_PASS)

# Charger template
templates = os.listdir("templates")
chosen_template = random.choice(templates)

with open(f"templates/{chosen_template}", "r", encoding="utf-8") as f:
    template = f.read()
rows = []

# Lire leads
with open("leads.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        rows.append(row)

sent_today = 0
MAX_PER_RUN = 20

log_file = open("logs.txt", "a", encoding="utf-8")

# Envoyer emails
for row in rows:
    if row["status"] == "NOT_SENT":
        personalized = template.replace("{{first_name}}", row["first_name"])
        personalized = personalized.replace("{{company}}", row["company"])

        msg = MIMEText(personalized)

        subjects = [
            f"Quick question {row['first_name']}",
            f"Hey {row['first_name']}",
            f"Question about {row['company']}"
        ]
        msg["Subject"] = random.choice(subjects)
        msg["From"] = EMAIL_USER
        msg["To"] = row["email"]

        server.send_message(msg)
        print(f"Sent to {row['email']}")
        time.sleep(20)

        log_file.write(f"{datetime.now()} - Sent to {row['email']}\n")

        row["status"] = "SENT"
        row["last_sent"] = datetime.now().isoformat()

        if sent_today >= MAX_PER_RUN:
            break
        sent_today += 1

        if TEST_MODE:
            print(personalized)
            continue

    if row["status"] == "SENT" and row["followup_sent"] == "NO":
        last_sent = datetime.fromisoformat(row["last_sent"])
        if datetime.now() - last_sent > timedelta(minutes=3):
                    personalized = f"Salut {row['first_name']}, je me permets de relancer 😊"

                    msg = MIMEText(personalized)
                    msg["Subject"] = f"Re: Quick question {row['first_name']}"
                    msg["From"] = EMAIL_USER
                    msg["To"] = row["email"]

                    server.send_message(msg)

                    row["followup_sent"] = "YES"
                    row["last_sent"] = datetime.now().isoformat()

                    print(f"Follow-up sent to {row['email']}")
            
# Sauvegarder CSV
with open("leads.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = ["first_name", "email", "company", "status", "last_sent","followup_sent"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

log_file.close()

server.quit()
print("Done.")
