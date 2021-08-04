// --------------------------------------------------------
// Node Express Simple Web Server  
// Licensed under The MIT License
// Written by Derek
// 2021-06-27
// --------------------------------------------------------

"use strict";
const express = require('express'); //express라이브러리 호출
const app = express();        // express 객체 생성
const webPort = 8000;
const fs = require('fs');     // 파일 처리 관련 라이브러리
const ejs = require('ejs');   // html파일에 JavaScript를 내장하여 서버에서 보낸 변수를 사용할 수 있음. 
const path = require('path'); // 경로 관련 라이브러리

// 정적(static) 경로 설정
app.use(express.static(path.join(__dirname,'public'))); // public 폴더 내에 있는 파일들은 브라우저에서 접근 가능

// 예제로 만든 api client에서 /test로 호출하면 test.html 파일과 tt 변수를 리턴함.
app.get('/test', (req, res) => {  
  fs.readFile('public/test.html', 'utf-8', function (error, data) {
    if(error) {
      console.log(error) 
      return;
    } else {
      let tt = 'text from sever'
      res.send(ejs.render(data, {
        text : tt
      }));
    }
  })
})

// 에러 처리 부분
app.use(function(req, res, next) {
  res.status(404).send('Sorry cant find that!');
});

app.use(function (err, req, res, next) {
  if(err){
      console.error(err.stack);
      console.log("error!!!!");
      res.status(500).send('Something broke!');
  }
});

app.listen(webPort, function(){
  console.log(`listening on ${webPort}`)
}); // 객체 맴버 함수 listen(서버띄울 포트번호, 띄운 후 실행할 코드) 서버 열기 