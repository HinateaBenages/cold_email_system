# cold_email_system
Scalable cold email system built for automated outreach with customizable templates and SMTP integration.

Cold Email System

A simple automated cold email system built for scalable outreach.

This project allows you to send personalized emails in bulk using SMTP.  
Built to explore how cold email automation works in practice.

Features
- Bulk email sending
- Personalization support
- SMTP integration
- Lead list support (CSV / JSON)
- Easy to customize

Setup

1. Clone the repository
   git clone <your-repo-url>
   cd cold-email-system

2. Install dependencies  
   Install the required packages depending on your stack (Python).

3. Configure email credentials  
   This project uses SMTP to send emails.

   Example SMTP settings:
   - Host: smtp.gmail.com
   - Port: 587
   - Encryption: TLS

4. Use an App Password (recommended)  
   If you're using Gmail or similar providers, do NOT use your main password.

   Instead:
   - Enable 2FA on your email account
   - Generate an App Password
   - Use the app password in your config or .env file

   Example:
   EMAIL_USER=your@email.com  
   EMAIL_PASS=your_app_password

5. Add your leads  
   Provide a CSV or JSON file containing recipient data (name, email, etc.).

6. Run the script  
   Start the sender and monitor logs/output.

Notes

- Never commit real credentials to the repository.
- Use a .env file and add it to .gitignore.
- Sending too many emails too fast can get your account flagged.

Disclaimer

This project is for educational and experimental purposes.  
Make sure you follow local email laws and anti-spam regulations.
