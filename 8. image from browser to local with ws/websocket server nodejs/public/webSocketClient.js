'use strict';

const wsid = '2'
const wstype = 'webc'
const url = 'ws://localhost:8000'
const wsk = new WebSocket(`${url}/wsid=${wsid}&wstype=${wstype}`); // ws
let wsStatus = false;

wsk.onopen = function () {
    console.log('서버와 웹 소켓 연결됨');
    wsk.send(JSON.stringify({
      optype: "init_websocket",   // optype    : 동작 유형(init_websocket 클라이언트에서 연결 완료 후 서버로 확인 메시지 전달)
      wsid:   wsid,               // wsid      : 해당 소켓 아이디
      wstype: wstype,             // wstype    : 소켓 접속 유형
      msg : "Hello Server ?",     // msg       : 메시지
      timestamp: timestamp()      // timestamp : 현재 시간
    }));
    wsStatus = true
};

wsk.onmessage = function (event) {

  let msgjson = JSON.parse(event.data);
  switch (msgjson.optype) {	
    case 'output': // msg 수신
      let imaget = "data:image/jpg;base64," + msgjson.frame;
      document.getElementById("myimage").src = imaget;
      break;
    default:
      console.log('optype error : ' + msgjson.optype)
      break;
  }
}

wsk.onclose = function () {
    console.log("disconnected websocket")
    wsStatus = false;    
}

function frame_capture() {
  const context = canvas.getContext('2d');
  context.drawImage(localVideo, 0, 0, width, height);
  
  if(wsStatus){
    let frame = canvas.toDataURL('image/jpg', 1.0)
    wsk.send(JSON.stringify({
      optype: "input",   
      wsid:   wsid,              
      wstype: wstype,             
      frame : frame,     
      timestamp: timestamp()      
    }))
  }
}

setInterval(function() { frame_capture();}, 100);
