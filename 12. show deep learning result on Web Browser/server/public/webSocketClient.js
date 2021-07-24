'use strict';

const wsid = '2'
const wstype = 'webc'
const url = 'ws://localhost:8000'
const wsk = new WebSocket(`${url}/wsid=${wsid}&wstype=${wstype}`); // ws

wsk.onopen = function () {
    console.log('서버와 웹 소켓 연결됨');
    wsk.send(JSON.stringify({
      optype: "init_websocket",   // optype    : 동작 유형(init_websocket 클라이언트에서 연결 완료 후 서버로 확인 메시지 전달)
      wsid:   wsid,               // wsid      : 해당 소켓 아이디
      wstype: wstype,             // wstype    : 소켓 접속 유형
      msg : "Hello Server ? I am web client!!", // msg       : 메시지
      timestamp: timestamp()      // timestamp : 현재 시간
    }));
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
}

