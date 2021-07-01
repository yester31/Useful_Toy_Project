"use strict"
module.exports = {

	timestamp:function() {
		let date = new Date();
		let year = date.getFullYear();              //yyyy
		let month = (1 + date.getMonth());          //M
		month = month >= 10 ? month : '0' + month;  //month 두자리로 저장
		let day = date.getDate();                   //d
		day = day >= 10 ? day : '0' + day;          //day 두자리로 저장
		let hours = date.getHours();                //h
		hours = hours >= 10 ? hours : '0' + hours;  //hours 두자리로 저장
		let min = date.getMinutes();                //m
		min = min >= 10 ? min : '0' + min;          //min 두자리로 저장
		let sec = date.getSeconds();                //s
		sec = sec >= 10 ? sec : '0' + sec;          //sec 두자리로 저장
		let msec = date.getMilliseconds()           //msec 세자리로 저장
		if(msec < 10){
			msec = '00' + msec;
		}else if(msec>=10 && msec<100){
			msec = '0' + msec;
		}
		return  year + '-' + month + '-' + day + ' ' + hours + ':' + min + ':' + sec  + '.' + msec;       //'-' 추가하여 yyyy-mm-dd 형태 생성 가능
	}
}