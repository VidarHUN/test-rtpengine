const Client = require('rtpengine-client').Client;
const client = new Client('127.0.0.1');
const fs = require('fs');

var myArgs = process.argv.slice(2);

var sdp = JSON.parse(fs.readFileSync(myArgs[2]).toString());

console.log(sdp);

client.answer(Number(myArgs[0]), myArgs[1], sdp)
    .then((res) => {
        console.log(res); // {"result": "ok", "sdp": "v=\0..."}
    })
    .catch((err) => {
        console.log(`Error: ${err}`);
    })

