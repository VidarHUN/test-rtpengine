import bencodepy # pip install bencode.py
import sdp_transform # pip install sdp-transform
import argparse
import json
import time
import subprocess
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
parser.add_argument('--file', '-f', type=str, dest='file', help="A simple file to list or query")
parser.add_argument('--ffmpeg', '-ff', type=int, choices=[1], dest='ffmpeg', 
                    help="If specified, it will start a certain number of ffmpeg processes")
parser.add_argument('--audio_file', '-af', type=str, dest='audio_file', help="Path of the audio to ffmpeg")
parser.add_argument('--tcpdump', '-t', type=str, dest='tcpdump', help='tcpdump interface')
parser.add_argument('--generate_calls', "-gc", type=int, dest='generate_calls', 
                    help='generate certain number of parallel calls with traffic')

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

# Send traffic to rtpengine
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

# Run a certain number of ffmpeg command 
def ffmpeg(cnt, offer_rtp_address, answer_rtp_address):
    procs = []
    for c in range(cnt):
        procs.append(subprocess.Popen(["ffmpeg", "-re", "-i", args.audio_file, "-ar", "8000", "-ac", "1", "-acodec", "pcm_mulaw", "-f", "rtp", offer_rtp_address[c]]))
        procs.append(subprocess.Popen(["ffmpeg", "-re", "-i", args.audio_file, "-ar", "8000", "-ac", "1", "-acodec", "pcm_mulaw", "-f", "rtp", answer_rtp_address[c]]))
    for proc in procs:
        proc.communicate()

# Run tcpdump in the background on a given interface
def tcpdump():
    return subprocess.Popen(["sudo", "tcpdump", "-i", args.tcpdump, "udp", "-vvn", "-w", "traffic.pcap"])

def generateAnswer(call_id, label, from_tag, to_tag, port):
    data = {}
    data["ICE"] = "remove"
    data["call-id"] = str(call_id)
    data["command"] = "answer"
    data["from-tag"] = str(from_tag)
    data["label"] = str(label)
    data["sdp"] = "v=0\r\no=- 1607446271 1 IN IP4 127.0.0.1\r\ns=tester\r\nt=0 0\r\nm=audio " + str(port) + " RTP/AVP 0\r\nc=IN IP4 127.0.0.1\r\na=sendrecv\r\na=rtcp:" + str(port + 1)
    data["to-tag"] = str(to_tag)
    return data

def generateOffer(call_id, label, from_tag, port):
    data = {}
    data["ICE"] = "remove"
    data["call-id"] = str(call_id)
    data["command"] = "offer"
    data["from-tag"] = str(from_tag)
    data["label"] = str(label)
    data["sdp"] = "v=0\r\no=- 1607444729 1 IN IP4 127.0.0.1\r\ns=tester\r\nt=0 0\r\nm=audio " + str(port) + " RTP/AVP 0\r\nc=IN IP4 127.0.0.1\r\na=sendrecv\r\na=rtcp:" + str(port + 1)
    return data

def generateCalls(cnt):
    start_port = 3000
    offers = []
    answers = []
    for _ in range(cnt):
        start_port += 2
        offer = send(generateOffer(str(start_port) + "-" + str(start_port + 2), "caller" + str(start_port), 
            "from-tag" + str(start_port), start_port), 
            "127.0.0.1", start_port)
        start_port += 2
        answer = send(generateAnswer(str(start_port - 2) + "-" + str(start_port), "callee" + str(start_port), 
            "from-tag" + str(start_port - 2), "to-tag" + str(start_port), start_port), 
            "127.0.0.1", start_port)
        parsed_offer = sdp_transform.parse(offer.get('sdp'))
        parsed_answer = sdp_transform.parse(answer.get('sdp'))
        offer_port = parsed_offer.get('media')[0].get('port')
        answer_port = parsed_answer.get('media')[0].get('port')
        
        offers.append("rtp://127.0.0.1:" + str(offer_port) + "?localrtpport=" + str(start_port - 2))
        answers.append("rtp://127.0.0.1:" + str(answer_port) + "?localrtpport=" + str(start_port))
    time.sleep(1)
    
    ffmpeg(cnt, offers, answers)


if args.tcpdump:
    tcpdump_proc = tcpdump()

if not args.server:
    if args.file:
        with open(args.file) as f:
            file = json.load(f)
        response = send(file, "127.0.0.1", 3000)
        print(response)
    # Read files
    if args.offer:
        with open(args.offer) as o:
            offer = json.load(o)
        response = send(offer, args.bind_offer[0], int(args.bind_offer[1]))
        parsed_sdp_dict = sdp_transform.parse(response.get('sdp'))
        offer_rtp_port = parsed_sdp_dict.get('media')[0].get('port')
        offer_rtcp_port = parsed_sdp_dict.get('media')[0].get('rtcp').get('port')
        print("RTP port from offer: %d" % offer_rtp_port)
        print("RTCP port from offer: %d" % offer_rtcp_port)
    if args.answer:
        with open(args.answer) as a:
            answer = json.load(a)
        response = send(answer, args.bind_answer[0], int(args.bind_answer[1]))
        parsed_sdp_dict = sdp_transform.parse(response.get('sdp'))
        answer_rtp_port = parsed_sdp_dict.get('media')[0].get('port')
        answer_rtcp_port = parsed_sdp_dict.get('media')[0].get('rtcp').get('port')
        print("RTP port from answer: %d" % answer_rtp_port )
        print("RTCP port from answer: %d" % answer_rtcp_port)
    if args.generate_calls:
        generateCalls(args.generate_calls)
else:
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

if args.offer and args.answer:
    time.sleep(1)
    offer_rtp_address = ["rtp://127.0.0.1:" + str(offer_rtp_port) + "?localrtpport=" + str(args.bind_offer[1])]
    answer_rtp_address = ["rtp://127.0.0.1:" + str(answer_rtp_port) + "?localrtpport=" + str(args.bind_answer[1])]
    ffmpeg(1, offer_rtp_address, answer_rtp_address)

if args.tcpdump:
    tcpdump_proc.terminate()

# TODO: Somehow make statistics about the traffic quality 
# Maybe you van use pyshark or a tcpdump subprocess
