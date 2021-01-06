#!/bin/bash
set -e

if [![-z "${TABLE}"]]; then
    modprobe xt_RTPENGINE
    sudo iptables -I INPUT -p udp -j RTPENGINE --id ${TABLE}
fi

exec "$@"

