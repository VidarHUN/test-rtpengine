#!/bin/bash

CALLER=$(node caller.js 22222 127.0.0.1 ../sdps/perl/caller.json);
echo "$CALLER";

CALLEE=$(node callee.js 22222 127.0.0.1 ../sdps/perl/callee.json);
echo "$CALLEE";

sudo ffmpeg -re -i ../audios/recording.wav -ar 8000 -ac 1 -acodec pcm_mulaw -f rtp "'rtp://127.0.0.1:${CALLER}?localrtpport=2000'" -ar 8000 -ac 1 -acodec pcm_mulaw -f rtp "'rtp://127.0.0.1:${CALLEE}?localrtpport=2004'"