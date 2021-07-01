"use strict";
const funcs = require('./public/libs');  // 커스텀 라이브러리 불러오기
const WebSocket = require('ws');         // 웹소켓 라이브러리
const Hashtable = require('jshashtable');// 해시테이블 라이브러리
const wshashtable = new Hashtable();     // 해시테이블 생성
global.wshashtable = wshashtable;     // 해시테이블 전역 변수화 시키기
const { v4: uuidV4 } = require('uuid');

module.exports = (server) => {
  const rooms = {};
  let roomID = 0 ;
  let socketid_;
  // 웹소켓 서버 객체 생성
  const wss = new WebSocket.Server({ server });
  // 클라이언트 접속할 경우 그 클라이언트와 연결된 소켓객체(ws) 생성 
  wss.on('connection', (ws, req) => {
    
    const uuID = uuidV4(); // create here a uuid for this connection
    ws.send(JSON.stringify({ 
      optype:"send_uuid",
      uuid : uuID,
      room : roomID,
      timestamp:funcs.timestamp()
    }))

    const leave = room => {
      // not present: do nothing
      if(! rooms[room][uuID]) return;
  
      // if the one exiting is the last one, destroy the room
      if(Object.keys(rooms[room]).length === 1) delete rooms[room];
      // otherwise simply leave the room
      else delete rooms[room][uuID];
    }

    // 웹 소켓 연결 시 클라이언트 정보 수집
    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    const port = req.headers['x-forwarded-port'] || req.socket.remotePort;
    console.log('새로운 클라이언트 접속', ip);

    // 사전에 약속된 규칙으로 소켓서버 호출하여 변수 생성
    let conuri =  req.url; //wss://192.168.31.26:8000/wsid=1234&wstype=type1 <- 예시 소켓 호출 (로컬에서는 ws)
    let wsid = conuri.replace(/.+wsid=([^&]+).*/,"$1");
    let wstype= conuri.replace(/.+wstype=([^&]+).*/,"$1");

    // 소켓 연결 정보 해시 테이블에 저장
    wshashtable.put(wstype + wsid, ws);  

    if(wstype == "c++ws"){
      ws.send(JSON.stringify({ 
        optype:"server_msg",
        wsid: "server1",                 
        wstype:"server",
        msg : "Hi? I am Server!!!",
        count : 5,
        timestamp:funcs.timestamp()
      }))
    }

    // 클라이언트로부터 메시지 수신 시
    ws.on('message', (fmessage) => {     
      let msgjson = null;             
      try {               
        // 전달 받은 문자열 메시지(fmessage)를 자바스크립트 객체로 변환 
        msgjson = JSON.parse(fmessage);       
      } catch (error) {
        // 전달 받은 문자열이 JSON 형식이 아니라면 에러가 catch 부분으로 들어오게 됨.
        //console.log(`[JSON 타입이 아닌 메시지 수신] error : ${error}`);	
      }      
      // JSON 형식의 문자열로 수신된 메시지만 처리 되도록 함.
      if(msgjson){ 		
        // API 정의서 프로토콜을 정상적으로 지켰다면 모든 소켓 메시지들은 optype이라는 구분자로 각각의 처리를 구분 한다. 
        switch (msgjson.optype) {	
          // 클라이언트로 부터 받은 연결 확인 메시지 처리 부분 
          case 'join': 
            try {
              socketid_= msgjson.socketid

              console.log(`[join] 메시지 : ${JSON.stringify(msgjson)}`);
              if(! rooms[msgjson.room]) {
                rooms[msgjson.room] = {}; // create the room
              }
              if(! rooms[msgjson.room][msgjson.uuid]) {
                rooms[msgjson.room][msgjson.uuid] = socketid_; // join the room  
              }
              // console.log(rooms[msgjson.room].keys())
              console.log(rooms) //
              //console.log(Object.keys(rooms[msgjson.room]).length) // room member number
              //console.log(rooms[msgjson.room]) // 
              //console.log(rooms[msgjson.room][msgjson.uuid])

              Object.values(rooms[msgjson.room]).forEach(function(member, index){
                console.log(member , index);
                wshashtable.get(member).send(JSON.stringify({ 
                  optype:"new-user-connected",
                  personN : socketid_, //new member
                  timestamp:funcs.timestamp()
                }))
              })
            }catch(error){
              console.log(`[join] error : ${error}`);
            }finally{
              break;
            }
          case 'leave':
            try {
              console.log(`[leave] 메시지 : ${JSON.stringify(msgjson.msg)}`);
              leave(room);
            }catch(error){
              console.log(`[leave] error : ${error}`);
            }finally{
              break;
            }
          
          default:
            // 약속된 optype이 아닌 경우 오류 메시지를 응답으로 전달
            console.log(`[잘못된 optype 수신] 전달 받은 optype과 매칭되는 api가 없습니다. : ${msgjson.optype}`);
            ws.send(`[잘못된 optype 수신] 전달 받은 optype과 매칭되는 api가 없습니다. : ${msgjson.optype}`);
            break;
        }
      }else{
        // 전달 받은 메시지가 JSON 타입이 아닐 경우 오류 메시지를 응답으로 전달
        console.log(`[JSON 타입이 아닌 메시지 수신]: (msg : ${fmessage}, ip : ${ip})`);
        ws.send(`[JSON 타입이 아닌 메시지 수신]: Successfully, a message has arrived. But this msg type is not JSON format. PLEASE SEND JSON TYPE FORMAT MESSAGE. (msg : ${fmessage}, ip : ${ip})`);
      }   
    });

    // 에러시
    ws.on('error', (error) => { 
      console.error(error);
    });

    // 연결 종료 시
    ws.on('close', () => {

      // for each room, remove the closed socket
      Object.values(rooms[roomID]).forEach(function(member, index){
        console.log(member , index);
        wshashtable.get(member).send(JSON.stringify({ 
          optype:"user-disconnected",
          socketID : socketid_, //new member
          timestamp:funcs.timestamp()
        }))
      })
      Object.values(rooms).forEach(room => leave(room));
      // 해시테이블에서 소켓 정보 제거 및 종료된 소켓 정보 출력
      wshashtable.remove(wstype + wsid);
      console.log(`[종료된 소켓 발생] ${funcs.timestamp()}`);   // 현재 시간 출력
      console.log(`[종료된 소켓 정보] 아이디 : ${wsid} / 접속 종류 : ${wstype} / 아이피 : ${ip} / 포트 : ${port}`);
      console.log(`[현재 접속 리스트] : ${wshashtable.keys()}`);

    });
  });
};