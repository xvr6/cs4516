# ICMP Pinger

This project implements a simple ICMP-based ping utility in Python. It sends ICMP Echo Request packets to a specified host and measures the round-trip time (RTT) for the responses. The program also calculates and displays statistics such as the minimum, maximum, and average RTT when terminated if the AF1 file is run.

## Features

- Sends ICMP Echo Request packets to a target host.
- Measures RTT for each response.
- Displays live ping results with RTT and TTL.
- Calculates and displays statistics (min, max, avg RTT) upon termination.

## Requirements

- Python 3.x
- Administrative/root privileges (required for raw socket operations).

## Files

- `icmp.py`: Basic implementation of the ICMP pinger.
- `icmp AF1.py`: Enhanced version with RTT statistics calculation.

## Usage

1. Run the script with administrative privileges:

   ```bash
   sudo python3 icmp.py
   ```

   or

   ```bash
   sudo python3 icmp\ AF1.py
   ```

2. The program will continuously ping `google.com` by default. You can modify the target host by changing the `ping("google.com")` line in the script.

3. To stop the program, press `Ctrl+C`. For `icmp AF1.py`, statistics will be displayed upon termination.

## Example Output

```txt
Pinging 142.251.167.138 using Python:

36 bytes from 142.251.167.138: time=20.504 ms TTL=102
36 bytes from 142.251.167.138: time=26.385 ms TTL=102
36 bytes from 142.251.167.138: time=19.587 ms TTL=102
36 bytes from 142.251.167.138: time=18.272 ms TTL=102
36 bytes from 142.251.167.138: time=19.633 ms TTL=102
36 bytes from 142.251.167.138: time=22.259 ms TTL=102
36 bytes from 142.251.167.138: time=21.942 ms TTL=102
36 bytes from 142.251.167.138: time=19.977 ms TTL=102
^C
```

If the AF1 version is run, you will also see:

```txt
--- Ping Statistics ---
Minimum RTT: 18.272 ms
Maximum RTT: 26.385 ms
Average RTT: 21.070 ms
```

## Notes

- The program uses raw sockets, which require administrative privileges.
- Ensure ICMP traffic is not blocked by your firewall or network configuration.