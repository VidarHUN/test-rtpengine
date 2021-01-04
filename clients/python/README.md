# Python client

usage: app.py 

[-h] [--port PORT] [--address ADDR] [--offer OFFER] \
[--answer ANSWER] [--bind_offer BIND_OFFER BIND_OFFER] \
[--bind_answer BIND_ANSWER BIND_ANSWER] [--file FILE] \
[--ffmpeg {1}] [--audio_file AUDIO_FILE] [--tcpdump TCPDUMP] \
[--generate_calls GENERATE_CALLS] [--pcap PCAP] [--server {0,1}] \
[--server_address SERVER_ADDRESS] [--server_port SERVER_PORT]

Control RTPengine through ng control.

optional arguments:

  **-h, --help**            show this help message and exit

  **--port PORT, -p PORT**  port of the running rtpengine

  **--address ADDR, -addr ADDR** address of the running rtpengine

  **--offer OFFER, -o OFFER** place of the offer JSON file

  **--answer ANSWER, -a ANSWER** place of the answer JSON file

  **--bind_offer BIND_OFFER BIND_OFFER, -bo BIND_OFFER BIND_OFFER** address port for offer source

  **--bind_answer BIND_ANSWER BIND_ANSWER, -ba BIND_ANSWER BIND_ANSWER** address port for answer source

  **--file FILE, -f FILE**  A simple file to list or query

  **--ffmpeg {1}, -ff {1}** If specified, it will start a certain number of ffmpeg processes

  **--audio_file AUDIO_FILE, -af AUDIO_FILE** Path of the audio to ffmpeg

  **--tcpdump TCPDUMP, -t TCPDUMP** tcpdump interface

  **--generate_calls GENERATE_CALLS, -gc GENERATE_CALLS** generate certain number of parallel calls with traffic

  **--pcap PCAP**           pcap file for analyze

  **--server {0,1}, -s {0,1}** 1 - proxy mode, 0 - simple mode

  **--server_address SERVER_ADDRESS, -sa SERVER_ADDRESS** listening address

  **--server_port SERVER_PORT, -sp SERVER_PORT** listening port