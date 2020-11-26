const Client = require('rtpengine-client').Client ;
const client = new Client() ;

// Simple ping-pong, check the service is alive and reachable 
client.ping(22222, '172.18.0.22')
 .then((res) => {
   console.log(`received ${JSON.stringify(res)}`); // {result: 'pong'}
 })
 .catch((err) => {
   console.log(`Error: ${err}`);
 })

