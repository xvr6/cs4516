import sys, socket
from ServerWorker import ServerWorker

class Server:	
	def main(self):
		"""Main method to start the server."""
		try:
			SERVER_PORT = int(sys.argv[1])  # Get the server port from command-line arguments
		except:
			print("[Usage: Server.py Server_port]\n")  # Print usage instructions if arguments are invalid
			return
		
		# Create and bind the RTSP socket
		rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		rtspSocket.bind(('', SERVER_PORT))
		rtspSocket.listen(5)  # Listen for incoming connections        

		# Accept client connections and handle them using ServerWorker
		while True:
			clientInfo = {}
			clientInfo['rtspSocket'] = rtspSocket.accept()  # Accept a client connection
			ServerWorker(clientInfo).run()  # Start a new thread to handle the client
			
if __name__ == "__main__":
	(Server()).main()  # Run the server

