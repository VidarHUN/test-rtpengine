const Client = require('rtpengine-client').Client;
const fs = require('fs');
const sdpTransform = require('sdp-transform');

var myArgs = process.argv.slice(2);

const CALLER_SDP = JSON.parse(fs.readFileSync(myArgs[2]).toString());

const PORT = Number(myArgs[0]);
const IP = myArgs[1];
const CALLER = new Client(2000, IP);

CALLER.offer(PORT, IP, CALLER_SDP)
    .then((res) => {
        let port = sdpTransform.parse(res.sdp).media[0].port;
        console.log(port);
        process.exit(1)
    })
    .catch((err) => {
        console.log(`Error: ${err}`);
    })