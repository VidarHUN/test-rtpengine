import bencodepy # pip install bencode.py
import sdp_transform # pip install sdp-transform
import argparse
import json
import time
import socket
import sys
import random
import string

# Parsing
parser = argparse.ArgumentParser(description='Control RTPengine through ng control.')
parser.add_argument('--port', '-p', default=22222, type=int, dest='port',
                    help='port of the running rtpengine')
parser.add_argument('--address', '-addr', default='127.0.0.1', type=str, dest='addr',
                    help='address of the running rtpengine')

# That's for local testing 
parser.add_argument('--offer', '-o', type=str, dest='offer', help='place of the offer JSON file')
parser.add_argument('--answer', '-a', type=str, dest='answer', help='place of the answer JSON file')
parser.add_argument('--bind_offer', '-bo', nargs=2, default=['127.0.0.1', '2000'], dest='bind_offer',
                    help='address port for offer source')
parser.add_argument('--bind_answer', '-ba', nargs=2, default=['127.0.0.1', '2004'], dest='bind_answer',
                    help='address port for answer source')

# Proxy part
parser.add_argument('--server', '-s', type=int, dest='server', choices=[0,1], 
                    help='1 - proxy mode, 0 - simple mode')
parser.add_argument('--server_address', '-sa', type=str, dest='server_address', 
                    help='listening address')
parser.add_argument('--server_port', '-sp', type=int, dest='server_port', 
                    help='listening port') 
args = parser.parse_args()

# Set up the bancode library
bc = bencodepy.Bencode(
    encoding='utf-8'
)

# Generate a random string for cookie 
def gen_cookie(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def send(file, bind_address, bind_port):
    # Open UDP4 socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((bind_address, bind_port))
    server_address = (args.addr, args.port)

    # Generate ng message
    cookie = gen_cookie(5)
    data = bencodepy.encode(file).decode() # Here goes all of the data, decode needed to remove b'

    # The ng protcol has two parts a cookie for responses and others and a
    # bencode dictinory which contain the data
    message = str(cookie) + " " + str(data)
    sent = sock.sendto(message.encode('utf-8'), server_address)

    data, server = sock.recvfrom(4096)
    data = data.decode()
    data = data.split(" ", 1)

    result = bc.decode(data[1])
    sock.close()
    
    return result

if not args.server:
    # Read files
    if args.offer:
        with open(args.offer) as o:
            offer = json.load(o)
        response = send(offer, args.bind_offer[0], int(args.bind_offer[1]))
        parsed_sdp_dict = sdp_transform.parse(response.get('sdp'))
        print("RTP port from offer: %d" % parsed_sdp_dict.get('media')[0].get('port'))
        print("RTCP port from offer: %d" % parsed_sdp_dict.get('media')[0].get('rtcp').get('port'))
    if args.answer:
        with open(args.answer) as a:
            answer = json.load(a)
        response = send(answer, args.bind_answer[0], int(args.bind_answer[1]))
        parsed_sdp_dict = sdp_transform.parse(response.get('sdp'))
        print("RTP port from answer: %d" % parsed_sdp_dict.get('media')[0].get('port'))
        print("RTCP port from answer: %d" % parsed_sdp_dict.get('media')[0].get('rtcp').get('port'))
else:
    IP = '127.0.0.1'
    PORT = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.server_address, args.server_port))
    print("Listening on %s:%d" % (args.server_address, args.server_port))
    while True:
        data, addr = sock.recvfrom(1024)
        time.sleep(1)
        response = send(json.loads(data.decode()), addr[0], int(addr[1]))
        parsed_sdp_dict = sdp_transform.parse(response.get('sdp'))
        print("RTP port from rtpengine: %d" % parsed_sdp_dict.get('media')[0].get('port'))
        print("RTCP port from rtpengine: %d\n" % parsed_sdp_dict.get('media')[0].get('rtcp').get('port'))

# TODO: Somehow make statistics about the traffic quality 
# Maybe you van use pyshark or a tcpdump subprocess
