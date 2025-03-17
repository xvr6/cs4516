import ssl
import base64
from socket import *

# Email credentials
sender_email = "xxx@gmail.com" #replace with your own gmail
receiver_email = "xxx@wpi.edu" #replace with your own WPI email
password = "xxx"  #replace with your own App password for your gmail; Use an app password instead of your actual gmail password
#create the App password here:
#https://support.google.com/accounts/answer/185833?visit_id=638759601307026124-2089972828&p=InvalidSecondFactor&rd=1

# Email content, replace with your own message and subject line
msg = "I love computer networks!"    
endmsg = #fill in start #fill in end   #denote the end of a message
subject = "Greetings To you!"

# specify Gmail SMTP server details
mailserver = #fill in start #fill in end
smtp_port = #fill in start #fill in end

# Create TCP socket (clientSocket) and establish a connection, and print out the response
#fill in start 
#fill in end
recv = clientSocket.recv(1024).decode()
print(recv)

# Secure connection with TLS by sending out Hello message (EHLO for TLS, not HELO) and print out the response
#fill in start 
#fill in end

#initiate a TLS (Transport Layer Security) handshake; STARTTLS command tells the server to start a TLS encryption
clientSocket.send(b"STARTTLS\r\n")
recv2 = clientSocket.recv(1024).decode()
print(recv2)

context = ssl.create_default_context()
clientSocket = context.wrap_socket(clientSocket, server_hostname=mailserver)

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
#fill in start 
#fill in end

# Send RCPT TO command and print out the response 
#fill in start 
#fill in end

# Send DATA command and print out the response 
#fill in start 
#fill in end

# Send email content, including subject, message, and endmsg, and print out the response 
#fill in start 
#fill in end

# Send QUIT command and print out the response
#fill in start 
#fill in end

# Close client socket
#fill in start 
#fill in end

