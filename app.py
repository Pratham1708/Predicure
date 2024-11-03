from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
import pandas as pd

app=Flask(__name__)
CORS(app)
model = pickle.load(open('model.pkl', 'rb'))
model_1=pickle.load(open('model_100.pkl','rb'))
# Load data
food = pd.read_csv('final_food_items.csv')
calorie = pd.read_csv('Calorie_value.csv')
diseases_data = pd.read_csv('diseases.csv')

# Functions
def calculate_bmr(weight, height, age, gender):
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == 'Female':
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return None
    return bmr

def calculate_calories(bmr, activity_level):
    if activity_level == 'Sedentary':
        pal = 1.2
    elif activity_level == 'Lightly':
        pal = 1.375
    elif activity_level == 'Moderately':
        pal = 1.55
    elif activity_level == 'Active':
        pal = 1.725
    elif activity_level == 'Extra':
        pal = 1.9
    else:
        return None
    calories = bmr * pal
    return calories

@app.route('/')
def hello():
    return render_template("index.html")

@app.route('/obesity_imp.html')
def hello1():
    return render_template("obesity_imp.html")

@app.route('/diabetes_imp.html')
def hello2():
    return render_template("diabetes_imp.html")

@app.route('/obesity_form.html')
def hello3():
    return render_template("obesity_form.html")

@app.route('/diabetes_form.html')
def hello4():
    return render_template("diabetes_form.html")

@app.route('/index.html')
def hello5():
    return render_template("index.html")

@app.route('/contact.html')
def hello6():
    return render_template("contact.html")

@app.route('/help.html')
def hello7():
    return render_template("help.html")

@app.route('/home.html')
def hello8():
    return render_template("home.html")

@app.route('/about.html')
def hello9():
    return render_template("about.html")

@app.route('/diet_form.html')
def hello10():
    return render_template("diet_form.html")

@app.route('/NutriGuide_imp.html')
def hello11():
    return render_template("NutriGuide_imp.html")

#@app.route('/submit',methods=['POST','GET'])
#def submit():
 #   if Request.method=='POST':
@app.route('/submit_1',methods=['POST'])
def submit_1():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model_1.predict(final_features)

    output = round(prediction[0], 2)
    if (output == 0):
        output = "Insufficient_Weight"
    elif(output == 1):
        output = "Normal Weight"
    elif(output == 2):
        output = "Overweight Level I"
    elif(output == 3):
        output = "Overweight Level II"
    elif(output == 4):
        output = "Obesity Type I"
    elif(output == 5):
        output = "Obesity Type II"                                
    else:
        output = "Obesity Type III"

    return render_template('obesity_form.html', prediction_text='You are most probably {}'.format(output))

@app.route('/submit',methods=['POST'])
def submit():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)
    if (output == 1):
        output = "Diabetic"
    elif(output==0):
        output = "Non diabetic"
    else:
        output="Pls enter correct information"

    return render_template('diabetes_form.html', prediction_text='You are mostly likely to be {}'.format(output))

@app.route('/recommendation', methods=['POST'])
def recommendation():
    # Get data from JSON
    data = request.json
    print(data)
    weight = float(data['weight'])
    height = float(data['height'])
    age = int(data['age'])
    gender = data['gender']
    activity_level = data['activity_level']
    pre_meal = data['pre_meal']
    num_diseases = int(data['num_diseases'])
    user_diseases = data['diseases']

    # Calculate BMR and calories
    bmr = calculate_bmr(weight, height, age, gender)
    if bmr is None:
        return jsonify({'error': 'Invalid input for BMR calculation'})
    calories = calculate_calories(bmr, activity_level)
    if calories is None:
        return jsonify({'error': 'Invalid input for calorie calculation'})
    
    # Calculate nutritional components based on diseases
    nutritional_components = []
    for disease in user_diseases:
        row = diseases_data.loc[diseases_data['Disease'] == disease]
        if not row.empty:
            nutritional_components.append(list(row.iloc[:, 1:].values[0]))

    final_list = nutritional_components[0] if nutritional_components else []
    for components in nutritional_components[1:]:
        final_list = [min(a, b) for a, b in zip(final_list, components)]

    # Adjust nutritional components based on calorie intake
    original_calories = 2200
    adjusted_list = [round(value * (calories / original_calories), 2) for value in final_list]

    # Categorize food items based on meal preference
    meal_categories = {
        'Vegetarian': ('Breakfast grains', 'Fruits', 'Vegetables', 'Protien', 'Healthy Fats','Breads','Juice','Indian bread','Tea & Coffee'),
        'Non-vegetarian': ('Breakfast grains', 'Fruits', 'Vegetables','Non-veg Protien','Protien', 'Healthy Fats','Breads','Juice','Indian bread','Tea & Coffee')
    }
    food_items_by_category = {category: [] for category in meal_categories.keys()}

    for food_item in food['food items']:
        category = calorie.loc[calorie['food items'] == food_item, 'Category'].values[0]
        for meal_category, categories in meal_categories.items():
            if category in categories and pre_meal == meal_category:
                food_items_by_category.setdefault(category, []).append(food_item)

    # Prepare response data
    response_data = {
        'bmr': bmr,
        'calories': calories,
        'adjusted_nutritional_components': adjusted_list,
        'food_items_by_category': food_items_by_category
    }

    return jsonify(response_data)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
