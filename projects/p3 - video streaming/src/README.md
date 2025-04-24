# Project 3 – Video Streaming with RTSP and RTP

## Goal

This project aims to help you understand video streaming implementation using the client-server model with RTSP and RTP protocols.

## Running the Code

1. **Start the Server**:
   ```bash
   python Server.py <server_port>
   ```
   Example:
   ```bash
   python Server.py 5678
   ```

2. **Start the Client**:
   ```bash
   python ClientLauncher.py <server_host> <server_port> <RTP_port> <video_file>
   ```
   Example:
   ```bash
   python ClientLauncher.py localhost 5678 6666 movie.Mjpeg
   ```

### RTSP Commands

- **SETUP**: Initializes the session and transport parameters.
- **PLAY**: Starts video playback.
- **PAUSE**: Pauses video playback.
- **TEARDOWN**: Terminates the session.

### Example Interaction

1. Client sends `SETUP` request.
2. Server responds with session details.
3. Client sends `PLAY` request to start playback.
4. Client can send `PAUSE` or `TEARDOWN` as needed.

### RTP Packetization

- Implement the `encode` function in `RtpPacket.py`:
  - Set RTP version to 2.
  - Set payload type to 26 (MJPEG).
  - Set sequence number, timestamp, and SSRC.

### Error Handling

- If the requested file is not found, the server sends a `404 NOT FOUND` response.
- For connection errors, the server sends a `500 CONNECTION ERROR` response.
