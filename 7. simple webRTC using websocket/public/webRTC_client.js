// Connect Client to the server socket, in this case, it's default '/'
// But usually server and client are hosted separately
// for ex: const socket = io('localhost:8080');
const yourVideoGrid = document.getElementById('your-video-grid');
const otherVideoGrid = document.getElementById('other-video-grid');
const myVideo = document.createElement('video');
const peers = {};

// check out more STUN servers: https://gist.github.com/zziuni/3741933
/**
 * Default config
  const DEFAULT_CONFIG = {
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "turn:0.peerjs.com:3478", username: "peerjs", credential: "peerjsp" }
  ],
  sdpSemantics: "unified-plan"
};
*/

const wsid = 'yhpark'
const wstype = 'webClinet'
const wsk = new WebSocket(`ws://localhost:8000/wsid=${wsid}&wstype=${wstype}`); // 웹소켓 연결 및 소켓 객체 생성
var myPeer = new RTCPeerConnection();

// 웹소켓 연결시
wsk.onopen = function () {
  console.log('[웹소켓 연결 성공]서버와 웹 소켓 연결됨');
};

// 웹소켓 메시지 수신할 경우 
wsk.onmessage = function (event) {
  let msgjson = null;      
  try {
    msgjson = JSON.parse(event.data); // 전달 받은 메시지 파싱 처리  
  } catch (error) {
    console.log(`This message is not JSON TYPE.`);	// 에러 메시지를 출력.
  }
  if(msgjson){
      switch (msgjson.optype) { 
        case 'send_uuid': // 'send_uuid'라는 optype의 메시지를 수신 할 경우 처리 로직
          console.log(`[send_uuid]   메시지 : ${event.data}`); 
          console.log(wsid);
          wsk.send(JSON.stringify({
            optype: "join",             // optype    : 동작 유형
            room: msgjson.room,            // roomid    : ROOM_ID
            socketid: wstype+wsid,         // socketid  : socketID
            uuid : msgjson.uuid,
            timestamp: timestamp()      // timestamp : 현재 시간
          }))
          break;  
        case 'user-disconnected': // 'user-disconnected'라는 optype의 메시지를 수신 할 경우 처리 로직
          console.log(`[user-disconnected]   메시지 : ${event.data}`);
          peers[msgjson.socketID].close();
          break;  
          // 1. Receive a signal from the server that a new user just joined
        case 'new-user-connected':
          console.log('new-user-connected')
          personN = msgjson.personN
          // 2 .call() share public IP and establish a connection
          // 3. myPeer call personN given my videoStream
          
          const call = myPeer.call(msgjson.personN, myStream);
          const personNVideo = document.createElement('video');
          // 6. AfterpersonN accept the call, myPeer will add personN's stream on myPeer's screen
          call.on('stream', (otherVideoStream) => {
              addVideoStream(personNVideo, otherVideoStream);
          });

          call.on('close', () => personNVideo.remove());

          peers[personN] = call;
          break; 

        default:
          console.log("default : ")
          break;
        }
  }else{
    console.log(`[JSON 타입이 아닌 메시지 수신]: (msg : ${event.data})`);
    wsk.send(`Successfully, a message has arrived. But this msg type is not JSON format. PLEASE SEND JSON TYPE FORMAT MESSAGE. (msg : ${event.data})`);
  }   
}

wsk.onclose = function () {
  console.log("disconnected websocket")
}

navigator.mediaDevices
    .getUserMedia({ video: true, audio: false })
    .then((myStream) => {
        // create your Video
        addVideoStream(myVideo, myStream, true);
        // Init "WAITING_CALL STATE" of current peer
        // 4. PersonN waiting for a call from (2)
        myPeer.on('call', (incomingCall) => {
            const personNVideo = document.createElement('video');
            // 5. personN answers the call given personN's Video Stream
            incomingCall.answer(myStream);

            // 6. personN now will add myPeer Stream to personN's screen
            incomingCall.on('stream', (otherVideoStream) => {
                addVideoStream(personNVideo, otherVideoStream);
            });
        });
    });

function addVideoStream(video, stream, yourVideo = false) {
    video.srcObject = stream;
    video.addEventListener('loadedmetadata', () => video.play());

    if (yourVideo) yourVideoGrid.append(video);
    else otherVideoGrid.append(video);
}
