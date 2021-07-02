"use strict";
const funcs = require('./public/libs');  // 커스텀 라이브러리 불러오기
const WebSocket = require('ws');         // 웹소켓 라이브러리
const Hashtable = require('jshashtable');// 해시테이블 라이브러리
const wshashtable = new Hashtable();     // 해시테이블 생성
global.wshashtable = wshashtable;     // 해시테이블 전역 변수화 시키기
const { v4: uuidV4 } = require('uuid');

module.exports = (server) => {
  // 웹소켓 서버 객체 생성
  const wss = new WebSocket.Server({ server });
  // 클라이언트 접속할 경우 그 클라이언트와 연결된 소켓객체(ws) 생성 
  wss.on('connection', (ws, req) => {

    // 웹 소켓 연결 시 클라이언트 정보 수집
    const ip = req.headers['x-forwarded-for'] || req.socket.remoteAddress;
    const port = req.headers['x-forwarded-port'] || req.socket.remotePort;
    console.log('새로운 클라이언트 접속', ip);
    // 사전에 약속된 규칙으로 소켓서버 호출하여 변수 생성
    let conuri =  req.url; //wss://192.168.31.26:8000/wsid=1234&wstype=type1 <- 예시 소켓 호출 (로컬에서는 ws)
    let wsid = conuri.replace(/.+wsid=([^&]+).*/,"$1");
    let wstype= conuri.replace(/.+wstype=([^&]+).*/,"$1");

    // 소켓 연결 정보 해시 테이블에 저장
    wshashtable.put(wsid, ws);  
    wshashtable.keys().forEach(key =>{
      console.log(key);
      wshashtable.get(key).send(
        JSON.stringify({'optype': 'ws_count' ,'ws_count': wshashtable.keys().length})
      )
    })
    // 클라이언트로부터 메시지 수신 시
    ws.on('message', (fmessage) => {  
      let msgjson = JSON.parse(fmessage); 
      //console.log(msgjson)        
      switch (msgjson.optype) {	
        case 'offer': 
          wshashtable.keys().forEach(key =>{
            wshashtable.get(key).send(fmessage)
          })
          break;
        case 'answer': 
          wshashtable.keys().forEach(key =>{
            wshashtable.get(key).send(fmessage)
          })
          break;
        case 'new-ice-candidate': 
          wshashtable.keys().forEach(key =>{
            wshashtable.get(key).send(fmessage)
          })
          break;
        default:
          console.log('optype error : ' + msgjson.optype)
        }
    });

    // 에러시
    ws.on('error', (error) => { 
      console.error(error);
    });

    // 연결 종료 시
    ws.on('close', () => {
      // 해시테이블에서 소켓 정보 제거 및 종료된 소켓 정보 출력
      wshashtable.remove(wstype + wsid);
      console.log(`[종료된 소켓 발생] ${funcs.timestamp()}`);   // 현재 시간 출력
      console.log(`[종료된 소켓 정보] 아이디 : ${wsid} / 접속 종류 : ${wstype} / 아이피 : ${ip} / 포트 : ${port}`);
      console.log(`[현재 접속 리스트] : ${wshashtable.keys()}`);

    });
  });
};