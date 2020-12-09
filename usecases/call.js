const Client = require('rtpengine-client').Client;
const fs = require('fs');
const sdpTransform = require('sdp-transform');

var myArgs = process.argv.slice(2);

const CALLER_SDP = JSON.parse(fs.readFileSync(myArgs[2]).toString());
const CALLEE_SDP = JSON.parse(fs.readFileSync(myArgs[3]).toString());

const PORT = Number(myArgs[0]);
const IP = myArgs[1];
const CALLER = new Client(2000, IP);
const CALLEE = new Client(2004, IP);

CALLER.offer(PORT, IP, CALLER_SDP)
    .then((res) => {
        let port = sdpTransform.parse(res.sdp).media[0].port;
        console.log("caller: " + port);
    })
    .catch((err) => {
        console.log(`Error: ${err}`);
    })

CALLEE.answer(PORT, IP, CALLEE_SDP)
    .then((res) => {
        let port = sdpTransform.parse(res.sdp).media[0].port;
        console.log("callee: " + port);
    })
    .catch((err) => {
        console.log(`Error: ${err}`);
    })