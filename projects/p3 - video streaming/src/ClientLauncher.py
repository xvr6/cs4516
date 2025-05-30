import sys
from tkinter import Tk
from Client import Client

if __name__ == "__main__":
	try:
		# Parse command-line arguments
		serverAddr = sys.argv[1]
		serverPort = sys.argv[2]
		rtpPort = sys.argv[3]
		fileName = sys.argv[4]	
	except IndexError:
		print("[Usage: ClientLauncher.py Server_name Server_port RTP_port Video_file]\n")	
		sys.exit(1)  # Exit if arguments are invalid
	
	root = Tk()  # Create the main GUI window
	
	# Create a new client instance
	app = Client(root, serverAddr, serverPort, rtpPort, fileName)
	app.master.title("RTPClient")	
	root.mainloop()  # Start the GUI event loop

