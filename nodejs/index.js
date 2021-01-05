const Client = require('rtpengine-client').Client ;
const client = new Client();

var myArgs = process.argv.slice(2);

// Simple ping-pong, check the service is alive and reachable 
client.ping(Number(myArgs[0]), myArgs[1])
 .then((res) => {
   console.log(`received ${JSON.stringify(res)}`); // {result: 'pong'}
 })
 .catch((err) => {
   console.log(`Error: ${err}`);
 })

