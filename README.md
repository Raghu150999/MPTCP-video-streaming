# MPTCP-Video-Streaming
Video Streaming implementation using MPTCP

## Requirements
1. Install MPTCP kernel from [here](https://multipath-tcp.org/pmwiki.php/Users/HowToInstallMPTCP?)
2. Install ffmpeg `sudo apt install ffmpeg`

## Usage
1. Start server: `python video_server.py`
2. Start client: `python video_client.py`

## Comments
1. Use mininet/netem for emulation
2. On wireshark, while recording packet trace, listen on interface *any to get multiple packets