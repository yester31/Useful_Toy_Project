"use strict";
const funcs = require('./public/libs');  // 커스텀 라이브러리 불러오기
const WebSocket = require('ws');         // 웹소켓 라이브러리
const Hashtable = require('jshashtable');// 해시테이블 라이브러리
const wshashtable = new Hashtable();     // 해시테이블 생성
//global.wshashtable = wshashtable;     // 해시테이블 전역 변수화 시키기
let wrtc = require('wrtc'); // webrtc 

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
      console.log("접속중인 소켓 아이디 :: " + key); 
      wshashtable.get(key).send(JSON.stringify({'optype': 'check_ws_num' ,'ws_count': wshashtable.keys().length}))
      console.log(key + " 로 업데이트된 웹소켓 접속수 전달")
    })


    const configuration = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]} // stun 서버 주소
    var peerConnection = new wrtc.RTCPeerConnection(configuration); // RTCPeerConnection객체 생성

    // 로컬 스트림을 track에 추가
    // localStream.getTracks().forEach(track => {
    //   console.log('add local stream to track!!')
    //   peerConnection.addTrack(track, localStream);
    //   console.log(localStream);
    // });      
    // var remoteVideo = document.querySelector('#remoteVideo');
    // // 원격에서 전달되는 스트림 수신하기 위해 새로 추가된 track이 있는지 확인하는 리스너
    // peerConnection.addEventListener('track', async (event) => {
    //   if(remoteVideo.srcObject !== event.streams[0]){
    //     remoteVideo.srcObject = event.streams[0];   // 새로 발생된 track의 원격 스트림을 화면에 출력 
    //     console.log('[Listener] find track and get remote stream !!')
    //     //console.log(event);
    //     console.log(event.streams[0])
    //   }
    // });
    // 로컬의 ICE 후보를 수집 하기 위해 icecandidate를 이벤트로 등록
    peerConnection.addEventListener('icecandidate', event => {
      if (event.candidate) {
        console.log('[Listener] find new icecandidate!!')
        ws.send(JSON.stringify({optype : 'new-ice-candidate', icecandidate : event.candidate, 'wsid' : 'server'})); // 발견된 ICE를 원격 피어로 전달
      }else{
        console.log('[Listener] All ICE candidates have been sent');
      }
    });
    // 연결 완료 상황을 알기 위해 connectionstatechange 이벤트 등
    peerConnection.addEventListener('connectionstatechange', event => {
      if (event) {
        console.log(`[Listener] 연결 상태 :: ${peerConnection.connectionState}`) // 연결 상태 체크
      }
    });
    async function getOffer(peerConnection){
      console.log("4. [호출측] 정보 준비 offer")
      const offer = await peerConnection.createOffer();   // 로컬에 대한 정보를 담은 객체 생성
      await peerConnection.setLocalDescription(offer);    // 이 객체를 로컬 설정에 등록
      //console.log(offer)
      return offer
    }
    async function treatOffer(peerConnection, offer){
      console.log("7. [수신측] 전달 받은 offer 내용을 수신측의 원격 정보로 등록.")
      await peerConnection.setRemoteDescription(new RTCSessionDescription(offer));// 전달 받은 호출 측 메타 정보를 이용하여 세션 객체로 생성하고 원격 설정 내용에 등록
      const answer = await peerConnection.createAnswer(); // 수신 측 피어에 대한 정보를 담은 객체 생성
      await peerConnection.setLocalDescription(answer);  // 수신 측 피어 로컬 정보에 위 객체를 등록
      return answer
    }
    async function treatAnswer(peerConnection, answer){
      console.log("10. [호출측] 전달 받은 answer 내용을 호출측의 원격 정보로 등록")
      //console.log(answer);
      const remoteDesc = await new RTCSessionDescription(answer); // 전달 받은 수신측 메타 정보로 세션 객체로 생성
      await peerConnection.setRemoteDescription(remoteDesc);  // 수신 측 세션 객체를 피어의 원격의 설정 내용에 등록
    }


    // 클라이언트로부터 메시지 수신 시
    ws.on('message', (fmessage) => {  
      let msgjson = JSON.parse(fmessage); 
      //console.log(msgjson)        
      switch (msgjson.optype) {	

        case 'send_ws_msg':
          console.log("send_ws_msg 요청 :: ")
          wshashtable.keys().forEach(key =>{
            if (key != msgjson.wsid ){
              wshashtable.get(key).send(fmessage)
            }
          })
          break;

        case 'initi_signal': 
          console.log("initi_signal 요청, ws_count ::" + wshashtable.keys().length);
          ws.send(JSON.stringify({'optype': 'initi_signal' ,'ws_count': wshashtable.keys().length}))
          break;

        case 'check_ws_num': 
          console.log("check_ws_num 요청, ws_count ::" + wshashtable.keys().length);
          ws.send(JSON.stringify({'optype': 'check_ws_num' ,'ws_count': wshashtable.keys().length}))
          break;

        case 'offer': 
          console.log("offer 요청 :: ")
          //console.log(msgjson.offer);
          wshashtable.keys().forEach(key =>{
            if (key == msgjson.wsid ){
              treatOffer(peerConnection, msgjson.offer)
              .then(answer =>{
                console.log("8. [수신측] 호출측으로 수신측의 peerConnection 정보가 담긴 answer 전달 ");
                wsk.send(JSON.stringify({'optype': 'answer' ,'answer': answer, 'wsid' : wsid}));  // 호출 측에 응답으로 수신측 피어에 대한 메타 정보를 전달
              })
              console.log(key + " 로 offer 전달")
            }
          })
          break;
        case 'answer': 
          console.log("answer 요청 :: ")
          wshashtable.keys().forEach(key =>{
            if (key == msgjson.wsid ){
              treatAnswer(peerConnection, msgjson.answer).then(()=>{
                console.log("11. [호출측] 수신받은 answer 처리 끝. :: ");
              })
              console.log(key + " 로 answer 전달")
            }          
          })
          break;
        case 'new-ice-candidate': 
          console.log("new-ice-candidate 요청 :: ")
          wshashtable.keys().forEach(key =>{
            if (key == msgjson.wsid ){
              peerConnection.addIceCandidate(msgjson.icecandidate); // 수신 받은 ICE를 등록
              console.log(key + " 로 new-ice-candidate 전달")
            }          
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
      wshashtable.remove(wsid);
      console.log(`[종료된 소켓 발생] ${funcs.timestamp()}`);   // 현재 시간 출력
      console.log(`[종료된 소켓 정보] 아이디 : ${wsid} / 접속 종류 : ${wstype} / 아이피 : ${ip} / 포트 : ${port}`);
      console.log(`[현재 접속 리스트] : ${wshashtable.keys()}`);
      wshashtable.keys().forEach(key =>{    
        wshashtable.get(key).send(JSON.stringify({'optype': 'check_ws_num' ,'ws_count': wshashtable.keys().length}))
        console.log(key + " 로 업데이트된 웹소켓 접속수 전달")
      })
    });
  });
};