const Client = require('rtpengine-client').Client ;
const client = new Client() ;

let sdp =   'v=0\r\n' +  
            'o=John 0844526 2890844526 IN IP4 172.18.0.1\r\n' +   
            's=-\r\n' +
            'c=IN IP4 172.18.0.1\r\n' + 
            't=0 0\r\n' +
            'e=valami\r\n' +
            'm=audio 6000 RTP/AVP 97 98\r\n' +  
            'a=rtpmap:97 AMR/16000/1\r\n' +
            'a=rtpmap:98 AMR-WB/8000/1';

console.log(sdp);

client.offer(22222, '172.18.0.22', {
    'sdp': `${sdp}`,
    'call-id': '1',
    'from-tag': '1'
    })
    .then((res) => {
        console.log(res); // {"result": "ok", "sdp": "v=\0..."}
    })
    .catch((err) => {
        console.log(`Error: ${err}`);
    })
