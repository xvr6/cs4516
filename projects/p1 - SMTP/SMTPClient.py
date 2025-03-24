import ssl
import base64
from socket import *

# Email credentials
sender_email = "" #TODO: replace with your own gmail
receiver_email = "" #TODO: replace with your own WPI email
password = ""  #TODO: replace with your own App password for your gmail; Use an app password instead of your actual gmail password
#create the App password here:
#https://support.google.com/accounts/answer/185833?visit_id=638759601307026124-2089972828&p=InvalidSecondFactor&rd=1

# Email content, replace with your own message and subject line
msg = "I love computer networks!"    
endmsg = "\r\n.\r\n"   #denote the end of a message
subject = "Greetings To you!"

# specify   details
mailserver = "smtp.gmail.com"
smtp_port = 587

# Create TCP socket (clientSocket) and establish a connection, and print out the response
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, smtp_port))
recv = clientSocket.recv(1024).decode()
print(recv)

# Secure connection with TLS by sending out Hello message (EHLO for TLS, not HELO) and print out the response
clientSocket.send(b"EHLO gmail.com\r\n")
recv = clientSocket.recv(1024).decode()
print(recv)

#initiate a TLS (Transport Layer Security) handshake; STARTTLS command tells the server to start a TLS encryption
clientSocket.send(b"STARTTLS\r\n")
recv2 = clientSocket.recv(1024).decode()
print(recv2)

# Wrap the socket with SSL
context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

# Send EHLO again after STARTTLS
clientSocket.send(b"EHLO gmail.com\r\n")
recv = clientSocket.recv(1024).decode()
print(recv)

# Authenticate
auth_command = "AUTH LOGIN\r\n"
clientSocket.send(auth_command.encode())
recv3 = clientSocket.recv(1024).decode()
print(recv3)

#send out email address for gmail
clientSocket.send(base64.b64encode(sender_email.encode()) + b"\r\n")
recv4 = clientSocket.recv(1024).decode()
print(recv4)

#send out password
clientSocket.send(base64.b64encode(password.encode()) + b"\r\n")
recv5 = clientSocket.recv(1024).decode()
print(recv5)

# Send MAIL FROM command, and print out the response 
clientSocket.send(f"MAIL FROM:<{sender_email}>\r\n".encode())
recv6 = clientSocket.recv(1024).decode()
print(recv6)

# Send RCPT TO command and print out the response 
clientSocket.send(f"RCPT TO:<{receiver_email}>\r\n".encode())
recv7 = clientSocket.recv(1024).decode()
print(recv7)

# Send DATA command and print out the response 
clientSocket.send(b"DATA\r\n")
recv8 = clientSocket.recv(1024).decode()
print(recv8)

# Send email content, including subject, message, and endmsg, and print out the response 
clientSocket.send(f"Subject: {subject}\r\n\r\n{msg}{endmsg}".encode())
recv9 = clientSocket.recv(1024).decode()
print(recv9)

# Send QUIT command and print out the response
clientSocket.send(b"QUIT\r\n")
recv10 = clientSocket.recv(1024).decode()
print(recv10)

# Close client socket
clientSocket.close()

