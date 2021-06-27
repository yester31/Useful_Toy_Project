"use strict";
const express = require('express'); //express라이브러리 호출
const app = express(); // express 객체 생성
const webPort = 8000;
const fs = require('fs');
const ejs = require('ejs');
const path = require('path');

// 정적(static) 경로 설정
app.use(express.static(path.join(__dirname,'public'))); // public 폴더 내에 있는 파일들은 브라우저에서 접근 가능

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

app.listen(webPort, function(){
  console.log(`listening on ${webPort}`)
}); // 객체 맴버 함수 listen(서버띄울 포트번호, 띄운 후 실행할 코드) 서버 열기 