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

const diseaseCountInput = document.getElementById("num_diseases");
const diseaseSelectsContainer = document.getElementById("diseases");

diseaseCountInput.addEventListener("change", () => {
  // Clear the existing select elements
  diseaseSelectsContainer.innerHTML = "";

  // Generate the specified number of select elements
  for (let i = 0; i < diseaseCountInput.value; i++) {
    const select = document.createElement("select");
    select.name = `disease-${i}`;
    select.id = `disease-${i}`;
    select.innerHTML = `
    <option value="">--Disease--</option>
      <option value="malnutrition">Malnutrition</option>
      <option value="diabetes">Diabetes</option>
      <option value="thyroid">Thyroid</option>
      <option value="heart-disease">Heart Disease</option>
      <option value="stroke">Stroke</option>
      <option value="kidney-diseases">Kidney Diseases</option>
      <option value="obese">Obese</option>
      <option value="overweight">Overweight</option>
    `;
    diseaseSelectsContainer.appendChild(select);
  }
});


