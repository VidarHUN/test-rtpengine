# Tried to send traffic with ffmpeg

## PCM RTP stream 

There is in audio file `audios/Recording.wav`. 

Start rtpdump like that: 

```
rtpdump -F hex -o pcm.rtp 127.0.0.1/10000
```
Thats will listen on port 10000 and write everything inside the `pcm.rtp` file.
Now you have to create the capturable stream with ffmpeg. 

```
ffmpeg -re -i audios/Recording.wav -ar 8000 -f rtp rtp://127.0.0.1:10000
```

## Connect Alice and Jhon

The only change to the original is the `m` and `a` field. 
Changed to this.

```
...
'm=audio 23000 RTP/AVP 0\r\n' +
'a=rtpmap:0 PCMU/8000/1\r\n' +
...
```

```
node lib/offer.js 22222 127.0.0.1 sdps/jhonpcm.json
node lib/offer.js 22222 127.0.0.1 sdps/alicepcm.json
```

## Send data 

```
sudo rtpsend -a -l -s 6000 -f pcm.rtp 127.0.0.1/23000  
```

Sadly this solution not works very well because the traffic not appear 
on port `7000`. The traffic goes into the rtpengine on port `6000`, but the 
rtpengine send back to `6000` instead of `7000`.