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
      msg : "Hello Server ? I am web client!!", // msg       : 메시지
      timestamp: timestamp()      // timestamp : 현재 시간
    }));
    wsStatus = true
};

wsk.onmessage = function (event) {
  let msgjson = JSON.parse(event.data);
  switch (msgjson.optype) {	
    case 'output': // python으로부터 이미지 수신
      let imaget = "data:image/jpg;base64," + msgjson.frame;  // img tag의 소스로 전달하기 위해 frame 정보에 헤더를 붙임
      document.getElementById("myimage").src = imaget;        // (4) 화면에 출력
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

const canvas = document.getElementById('canvas');
const width = 350;
const height = 260;

function frame_capture() {
  const context = canvas.getContext('2d'); // canvas에 그려질 이미지를 2d로 값 설정
  context.drawImage(localVideo, 0, 0, width, height); // video tag의 영상을 canvas의 이미지로 갖고 온다. (2)출력
  if(wsStatus){ // 웹소켓이 연결 되었을때만 전송
    let frame = canvas.toDataURL('image/jpg', 1.0) // canvas에 그려진 이미지(base64 형태 소스)를 frame 변수에 담는다.
    wsk.send(JSON.stringify({ 
      optype: "input",   
      wsid:   wsid,              
      wstype: wstype,             
      frame : frame,     
      timestamp: timestamp()      
    }))
  }
}

setInterval(function() { frame_capture();}, 100); // 100ms마다 frame_capture() 함수 수행
