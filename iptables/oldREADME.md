# Measure latency and jitter

## Without iptables

The rtpengine config: 

```
[rtpengine]
interface=127.0.0.1
foreground=true
log-stderr=true
listen-ng=127.0.0.1:22222
port-min=23000
port-max=32768
recording-dir=/tmp
recording-method=pcap
recording-format=eth
log-level=6
delete-delay=0
timeout=600
```

Control output:

```
$ python python/app.py -o sdps/perl/caller.json -a sdps/perl/callee.json
RTP port from offer: 23000
RTCP port from offer: 23001
RTP port from answer: 23018
RTCP port from answer: 23019

```

Traffic generators:

```
sudo ffmpeg -re -i audios/recording.wav -ar 8000 -ac 1 -acodec pcm_mulaw -f rtp 'rtp://127.0.0.1:23000?localrtpport=2000' 

sudo ffmpeg -re -i audios/recording.wav -ar 8000 -ac 1 -acodec pcm_mulaw -f rtp 'rtp://127.0.0.1:23018?localrtpport=2004'
```

Used tcpdump command: 

```
sudo tcpdump -i lo udp -vvn -w traffic.pcap  
```

rtpengine output: 

```
sudo rtpengine --config-file sample-rtpengine.conf
[sudo] password for richard: 
[1607691988.600169] INFO: Generating new DTLS certificate
[1607691988.648692] INFO: Startup complete, version 9.2.0.0+0~mr9.2.0.0 git-master-440ca5ac
[1607692000.155104] INFO: [0.5423403855684267]: Received command 'offer' from 127.0.0.1:2000
[1607692000.155163] NOTICE: [0.5423403855684267]: Creating new call
[1607692000.155348] INFO: [0.5423403855684267]: Replying to 'offer' from 127.0.0.1:2000 (elapsed time 0.000226 sec)
[1607692000.158021] INFO: [0.5423403855684267]: Received command 'answer' from 127.0.0.1:2004
[1607692000.158068] INFO: [0.5423403855684267]: Replying to 'answer' from 127.0.0.1:2004 (elapsed time 0.000036 sec)
[1607692006.920108] INFO: [0.5423403855684267 port 23001]: Confirmed peer address as 127.0.0.1:2001
[1607692006.920139] INFO: [0.5423403855684267 port 23000]: Confirmed peer address as 127.0.0.1:2000
[1607692007.052763] INFO: [0.5423403855684267 port 23000]: Confirmed peer address as 127.0.0.1:2000
[1607692012.048012] INFO: [0.5423403855684267 port 23001]: Confirmed peer address as 127.0.0.1:2001
[1607692014.674041] INFO: [0.5423403855684267 port 23019]: Confirmed peer address as 127.0.0.1:2005
[1607692014.674044] INFO: [0.5423403855684267 port 23018]: Confirmed peer address as 127.0.0.1:2004
[1607692014.734503] INFO: [0.5423403855684267 port 23000]: Confirmed peer address as 127.0.0.1:2000
[1607692014.806543] INFO: [0.5423403855684267 port 23018]: Confirmed peer address as 127.0.0.1:2004
[1607692017.167251] INFO: [0.5423403855684267 port 23001]: Confirmed peer address as 127.0.0.1:2001
[1607692019.799730] INFO: [0.5423403855684267 port 23019]: Confirmed peer address as 127.0.0.1:2005
^C[1607692057.166777] INFO: Version 9.2.0.0+0~mr9.2.0.0 git-master-440ca5ac shutting down
```
Details

- jitter: mean value 
- delta: max value

| Direction   | Forward Jitter(ms) | Forward Delta(ms) | Reverse Jitter(ms) | Reverse Delta(ms) |
|-------------|--------------------|-------------------|--------------------|-------------------|
| 2000-23000  | 4.88               | 135.47            | 4.81               | 133.17            |
| 2004-23018  | 4.82               | 133.03            | 4.88               | 133.30            |

Found pcap [here](./no_iptables.pcap)

## With iptables

Start rtpengine

```
modprobe xt_RTPENGINE
iptables -I INPUT -p udp -j RTPENGINE --id 0

rtpengine --table=0 --interface=127.0.0.1 --listen-ng=127.0.0.1:22222 --tos=184 --pidfile=/run/rtpengine.pid --no-fallback
```

Log of rtpengine: 

```
Dec 11 14:45:11 Aspire-A315 rtpengine[5664]: INFO: Generating new DTLS certificate
Dec 11 14:45:11 Aspire-A315 rtpengine[5665]: INFO: Startup complete, version 9.2.0.0+0~mr9.2.0.0 git-mas
ter-440ca5ac
Dec 11 14:49:51 Aspire-A315 rtpengine[5665]: INFO: [0.5423403855684267]: Received command 'offer' from 1
27.0.0.1:2000
Dec 11 14:49:51 Aspire-A315 rtpengine[5665]: NOTICE: [0.5423403855684267]: Creating new call
Dec 11 14:49:51 Aspire-A315 rtpengine[5665]: INFO: [0.5423403855684267]: Replying to 'offer' from 127.0.
0.1:2000 (elapsed time 0.000188 sec)
Dec 11 14:49:51 Aspire-A315 rtpengine[5665]: INFO: [0.5423403855684267]: Received command 'answer' from
127.0.0.1:2004
Dec 11 14:49:51 Aspire-A315 rtpengine[5665]: INFO: [0.5423403855684267]: Replying to 'answer' from 127.0
.0.1:2004 (elapsed time 0.000037 sec)
Dec 11 14:50:30 Aspire-A315 rtpengine[5665]: INFO: [0.5423403855684267 port 30001]: Confirmed peer addre
ss as 127.0.0.1:2001
Dec 11 14:50:30 Aspire-A315 rtpengine[5665]: INFO: [0.5423403855684267 port 30000]: Confirmed peer addre
ss as 127.0.0.1:2000
```

The other commands are the same except of the ports. 

Details

- jitter: mean value 
- delta: max value

| Direction   | Forward Jitter(ms) | Forward Delta(ms) | Reverse Jitter(ms) | Reverse Delta(ms) |
|-------------|--------------------|-------------------|--------------------|-------------------|
| 2000-30000  | 4.92               | 134.98            | 4.93               | 133.15            |
| 2004-30020  | 4.93               | 133.16            | 4.90               | 134.96            |

Found pcpa [here](./iptables.pcap)