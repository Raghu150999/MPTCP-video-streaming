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
2. On wireshark, while recording packet trace, listen on interface *any to get packets from different interfaces.

## Disable an interface from using MPTCP
`ip link set dev eth0 multipath off`

*Note: here `eth0` is the interface name*

## emulation
`sudo tc qdisc add dev lo root netem loss 10% delay 20ms 5ms distribution pareto`