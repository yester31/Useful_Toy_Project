'use strict';

// Video element where stream will be placed.
const localVideo = document.getElementById('local');

const Constraints = { video: true, audio: false  };
navigator.mediaDevices.getUserMedia(Constraints) // 1. 호출 후 브라우저는 사용자에게 카메라에 액세스 할 수 있는 권한을 요청
  .then(stream =>{                  // 2. stream을 가져옴
    localVideo.srcObject = stream;  // 3. srcObject속성을 통해 로컬 스트림을 (1) 화면에 출력
  })
  .catch(error =>{ // 2. 실패 할경우 에러 메시지 출력
    console.log('navigator.getUserMedia error: ', error);
  });