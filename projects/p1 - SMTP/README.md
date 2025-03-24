# SMTP Client

This project demonstrates how to send an email using Python's socket library and the SMTP protocol.

## How to Run

1. **Install Dependencies**: Ensure you have Python installed on your system. This script uses the `ssl` and `socket` libraries, which are included in the Python Standard Library.

2. **Edit the Script**: Open `SMTPClient.py` and replace the following placeholders with your information:
   - `sender_email`: Your Gmail address.
   - `receiver_email`: Your WPI email address.
   - `password`: Your Gmail App password. Follow the instructions [here](https://support.google.com/accounts/answer/185833?visit_id=638759601307026124-2089972828&p=InvalidSecondFactor&rd=1) to create an App password.

3. **Run the Script**: Execute the script using Python.
   ```sh
   python SMTPClient.py
   ```

## Email Content

The email content is defined within the script:
- `msg`: The body of the email.
- `subject`: The subject line of the email.

Feel free to modify these variables to customize your email message.

## Example

```python
# Email credentials
sender_email = "your_gmail@gmail.com"
receiver_email = "your_wpi_email@wpi.edu"
password = "your_app_password"

# Email content
msg = "I love computer networks!"
subject = "Greetings To you!"
```

After making these changes, run the script to send an email from your Gmail account to your WPI email account.
