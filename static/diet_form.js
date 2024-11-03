// Your existing step navigation code
var step1 = document.getElementById("step1");
var step2 = document.getElementById("step2");
var step3 = document.getElementById("step3");
var progress = document.getElementById("progress");

var Next1 = document.getElementById("Next1");
var Next2 = document.getElementById("Next2");
var Previous1 = document.getElementById("Previous1");
var Previous2 = document.getElementById("Previous2");
var Submit = document.getElementById("submit");

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

// Your existing disease selection code
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

// Add form submission handling
document.querySelector('form').addEventListener('submit', function(e) {
    e.preventDefault();

    // Get all disease selections
    const diseaseSelects = Array.from(diseaseSelectsContainer.getElementsByTagName('select'));
    const selectedDiseases = diseaseSelects.map(select => select.value).filter(value => value !== "");

    // Get form data
    const formData = {
        weight: document.getElementById('weight').value,
        height: document.getElementById('height').value,
        age: document.getElementById('age').value,
        gender: document.getElementById('gender').value,
        activity_level: document.getElementById('activity_level').value,
        pre_meal: document.getElementById('pre_meal').value,
        num_diseases: diseaseCountInput.value,
        diseases: selectedDiseases
    };

    // Send POST request
    fetch('/recommendation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Create results container if it doesn't exist
        let resultsContainer = document.getElementById('results');
        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'results';
            resultsContainer.className = 'container mt-4';
            document.querySelector('.cont').insertAdjacentElement('afterend', resultsContainer);
        }

        // Display results
        resultsContainer.style.display = 'block';
        resultsContainer.innerHTML = `
            <h3>Your Diet Recommendations</h3>
            <div class="row">
                <div class="col-md-6">
                    <h4>BMR and Calorie Information</h4>
                    <p>BMR: ${Math.round(data.bmr)} calories</p>
                    <p>Daily Calorie Requirement: ${Math.round(data.calories)} calories</p>
                </div>
            </div>
            
            <div class="row mt-4">
                <div class="col-12">
                    <h4>Weekly Diet Charts</h4>
                    <div id="diet-charts"></div>
                </div>
            </div>
        `;

        // Display diet charts
        const dietChartsDiv = document.getElementById('diet-charts');
        data.weekly_diet_charts.forEach((weekChart, weekIndex) => {
            const weekDiv = document.createElement('div');
            weekDiv.className = 'mb-4';
            weekDiv.innerHTML = `<h5>Week ${weekIndex + 1}</h5>`;
            
            const table = document.createElement('table');
            table.className = 'table table-bordered';
            
            // Add table header
            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th>Day</th>
                    <th>Breakfast</th>
                    <th>Lunch</th>
                    <th>Snacks</th>
                    <th>Dinner</th>
                </tr>
            `;
            table.appendChild(thead);
            
            // Add table body
            const tbody = document.createElement('tbody');
            weekChart.forEach(day => {
                const row = document.createElement('tr');
                day.forEach(meal => {
                    const cell = document.createElement('td');
                    cell.textContent = meal;
                    row.appendChild(cell);
                });
                tbody.appendChild(row);
            });
            table.appendChild(tbody);
            
            weekDiv.appendChild(table);
            dietChartsDiv.appendChild(weekDiv);
        });

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while generating diet recommendations.');
    });
});
