const Client = require('rtpengine-client').Client;
const client = new Client();

var myArgs = process.argv.slice(2);

// console.log(`${myArgs[2]}`);

client.query(Number(myArgs[0]), myArgs[1],{
    'call-id':'0.5423403855684267',
    'from-tag':'0.4166036407436595',
    })
    .then((res) => { console.log(res); })
    .catch((err) => { console.log(`Error: ${err}`); })
