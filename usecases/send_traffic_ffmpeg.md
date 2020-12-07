# Send traffic with ffmpeg

## Make a call with Jhon and Alice 

Jhon make an **offer**: 

```
node lib/offer.js 22222 127.0.0.1 sdps/offer/jhonpcm.json
```

And Alice **answer** it:

```
node lib/answer.js 22222 127.0.0.1 sdps/answer/alice_pcm_answer.json
```

Your can make a query and see if they are in a call:

```
node lib/query.js 22222 127.0.0.1
```

## Send traffic with ffmpeg

They are use **PCMU** codecs, so you have to generate PCMU RTP traffic. 


```
ffmpeg -re -i audios/recording.wav -ar 8000 -ac 1 -acodec pcm_mulaw -f rtp rtp://127.0.0.1:23000
```

This is a *wav* audio file with the following settings: 

- **-ar** Audio sampling fraquency 
- **-ac** Number of audio channels
- **-acodec** Set the audio codec
- **-f** Output

If you are capture data with **tcpdump** like that: 

```
sudo tcpdump -i lo udp -vvn -w traffic.pcap
```

You can play the audio on **Alice** side, but if you want to send traffic 
to **Jhon** the traffic will remain on Alice side and Jhon will not hear 
anything. 