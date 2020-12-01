# Test setup for use rtpengine with rtpengine-client

Start rtpengine with `--log-level=7` to see everything and use 
the `sample-rtpengine.conf`. 

```
sudo rtpengine --config-file sample-rtpengine.conf --log-level=7
```

Thats  will listen on `localhost:22222` so you have to use that
address. 

Connect with clients:

John: 

```
node lib/offer.js 22222 127.0.0.1 /home/richard/Desktop/Ericsson/test-rtpengine/sdps/jhon.json
```

Answer: 

```json
{
  sdp: 'v=0\r\n' +
    'o=John 0844526 2890844526 IN IP4 127.0.0.1\r\n' +
    's=-\r\n' +
    'c=IN IP4 127.0.0.1\r\n' +
    't=0 0\r\n' +
    'm=audio 23000 RTP/AVP 97 98\r\n' +
    'a=rtpmap:97 AMR/16000/1\r\n' +
    'a=rtpmap:98 AMR-WB/8000/1\r\n' +
    'a=sendrecv\r\n' +
    'a=rtcp:23001\r\n',
}
```
Please notice the `'m=audio 23000 RTP/AVP 97 98\r\n'` line because later you have to send 
traffic to that port. This field could be different on each run. 

Alice:

```
node lib/offer.js 22222 127.0.0.1 /home/richard/Desktop/Ericsson/test-rtpengine/sdps/alice.json
```

Answer: 

```json
{
  sdp: 'v=0\r\n' +
    'o=Alice 0844516 2890844516 IN IP4 127.0.0.1\r\n' +
    's=-\r\n' +
    'c=IN IP4 127.0.0.1\r\n' +
    't=0 0\r\n' +
    'm=audio 23024 RTP/AVP 97 98\r\n' +
    'a=rtpmap:97 AMR/16000/1\r\n' +
    'a=rtpmap:98 AMR-WB/8000/1\r\n' +
    'a=sendrecv\r\n' +
    'a=rtcp:23025\r\n',
  result: 'ok'
}
```

Please notice the `'m=audio 23024 RTP/AVP 97 98\r\n'` line because later you have to send 
traffic to that port. This field could be different on each run. 

Now you can send traffic through `rtpengine`, but now this will only appear as 
some garbage data what the client can't decode. 

Send traffic: 

```
sudo /usr/local/bin/rtpsend -a -l -s 6000 -f rtp_files/amrnb_fv_to_mrsv0.hex.rtp 127.0.0.1/23000
```

Notice that, the destination address is the `m` field in Jhon's answer. 

Currently you can check the traffic flow with `socat`, because the client will fail 
while trying to decode the message. 

```
socat -d udp-l:7000 -  
```

You should see some garbage when the `rtpsend` starts. 

Let's see what will record the `rtpdump` on port 7000. 

```
rtpdump -o dump.rtp 127.0.0.1/7000
```

The following rtp file generated without any data per record: 

```
1606822194.838536 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=1 pt=127 ((null),0,0) seq=15613 ts=1628629055 ssrc=0x76832b0c 
1606822194.859002 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15614 ts=1628629215 ssrc=0x76832b0c 
1606822194.877622 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15615 ts=1628629375 ssrc=0x76832b0c 
1606822194.898746 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15616 ts=1628629535 ssrc=0x76832b0c 
1606822194.917935 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15617 ts=1628629695 ssrc=0x76832b0c 
1606822194.938082 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15618 ts=1628629855 ssrc=0x76832b0c 
1606822194.958229 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15619 ts=1628630015 ssrc=0x76832b0c 
1606822194.977806 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15620 ts=1628630175 ssrc=0x76832b0c 
1606822195.002115 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15621 ts=1628630335 ssrc=0x76832b0c 
1606822195.017860 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15622 ts=1628630495 ssrc=0x76832b0c 
1606822195.039562 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15623 ts=1628630655 ssrc=0x76832b0c 
1606822195.057878 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15624 ts=1628630815 ssrc=0x76832b0c 
1606822195.083696 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15625 ts=1628630975 ssrc=0x76832b0c 
1606822195.098646 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15626 ts=1628631135 ssrc=0x76832b0c 
1606822195.118599 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15627 ts=1628631295 ssrc=0x76832b0c 
1606822195.138673 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15628 ts=1628631455 ssrc=0x76832b0c 
1606822195.158367 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15629 ts=1628631615 ssrc=0x76832b0c 
1606822195.179924 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15630 ts=1628631775 ssrc=0x76832b0c 
1606822195.202116 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15631 ts=1628631935 ssrc=0x76832b0c 
1606822195.219403 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15632 ts=1628632095 ssrc=0x76832b0c 
1606822195.238925 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15633 ts=1628632255 ssrc=0x76832b0c 
1606822195.259999 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15634 ts=1628632415 ssrc=0x76832b0c 
1606822195.278216 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15635 ts=1628632575 ssrc=0x76832b0c 
1606822195.299299 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15636 ts=1628632735 ssrc=0x76832b0c 
1606822195.318932 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15637 ts=1628632895 ssrc=0x76832b0c 
1606822195.340076 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15638 ts=1628633055 ssrc=0x76832b0c 
1606822195.357984 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15639 ts=1628633215 ssrc=0x76832b0c 
1606822195.378104 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15640 ts=1628633375 ssrc=0x76832b0c 
1606822195.399046 RTP len=19 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15641 ts=1628633535 ssrc=0x76832b0c 
1606822195.458333 RTP len=19 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=0 pt=127 ((null),0,0) seq=15642 ts=1628634015 ssrc=0x76832b0c 
1606822195.558175 RTP len=45 from=127.0.0.1:23014 v=2 p=0 x=0 cc=0 m=1 pt=127 ((null),0,0) seq=15643 ts=1628634815 ssrc=0x76832b
```

No `data` field could be a problem! 