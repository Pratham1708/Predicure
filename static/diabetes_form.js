var step1 = document.getElementById("step1");
var step2 = document.getElementById("step2");
var step3 = document.getElementById("step3");

var Next1 = document.getElementById("Next1");
var Next2 = document.getElementById("Next2");
var Previous1 = document.getElementById("Previous1");
var Previous2 = document.getElementById("Previous2");

Next1.onclick = function(){
   step1.style.top = "-550px";
   step2.style.top = "100px";
   progress.style.width = "340px";
}
Previous1.onclick = function(){
   step1.style.top = "100px";
   step2.style.top = "550px";
   progress.style.width = "170px";
}
Next2.onclick = function(){
   step2.style.top = "-550px";
   step3.style.top = "100px";
   progress.style.width = "510px";
}
Previous2.onclick = function(){
   step2.style.top = "100px";
   step3.style.top = "550px";
   progress.style.width = "340px";
}
