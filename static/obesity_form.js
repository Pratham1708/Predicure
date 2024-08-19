var step1 = document.getElementById("step1");
var step2 = document.getElementById("step2");
var step3 = document.getElementById("step3");
var step4 = document.getElementById("step4");

var Next1 = document.getElementById("Next1");
var Next2 = document.getElementById("Next2");
var Next3 = document.getElementById("Next3");
var Previous1 = document.getElementById("Previous1");
var Previous2 = document.getElementById("Previous2");
var Previous3 = document.getElementById("Previous3");

Next1.onclick = function(){
   step1.style.top = "-600px";
   step2.style.top = "100px";
   progress.style.width = "340px";
}
Previous1.onclick = function(){
   step1.style.top = "100px";
   step2.style.top = "600px";
   progress.style.width = "170px";
}
Next2.onclick = function(){
   step2.style.top = "-600px";
   step3.style.top = "100px";
   progress.style.width = "510px";
}
Previous2.onclick = function(){
   step2.style.top = "100px";
   step3.style.top = "600px";
   progress.style.width = "340px";
}
Next3.onclick = function(){
    step3.style.top = "-600px";
    step4.style.top = "100px";
    progress.style.width = "680px";
}
 Previous3.onclick = function(){
    step3.style.top = "100px";
    step4.style.top = "600px";
    progress.style.width = "510px";
}