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
        nutritional_components.append(list(row.iloc[:, 1:].values[0]))

    final_list = nutritional_components[0]
    for components in nutritional_components[1:]:
        for i, value in enumerate(components):
            final_list[i] = min(final_list[i], value)

    # Adjust nutritional components based on calorie intake
    original_calories = 2200
    adjusted_list = [round(value * (calories / original_calories), 2) for value in final_list]

    # Find food items that match the nutritional requirements
    food_items_dict = {}
    for i, component_value in enumerate(final_list):
        component_name = diseases_data.columns[i+1]
        food_items = []
        for index, row in food.iterrows():
            food_component_value = row[component_name]
            if abs(float(food_component_value) - float(component_value)) / float(component_value) <= 0.90:
                food_items.append(row['food items'])
        food_items_dict[component_name] = food_items

    food_i_list = list(food_items_dict.values())
    food_i_list = sum(food_i_list, [])
    unique_list = list(set(food_i_list))

    # Generate weekly diet chart
    weekly_diet_charts = []
    for week in range(3):  # Generate 3 weeks of diet charts
        weekly_diet_chart = generate_weekly_diet_chart(pre_meal)
        weekly_diet_charts.append(weekly_diet_chart)

    # Prepare response data
    response_data = {
        'bmr': bmr,
        'calories': calories,
        'adjusted_nutritional_components': adjusted_list,
        'recommended_food_items': unique_list,
        'weekly_diet_charts': weekly_diet_charts
    }

    return jsonify(response_data)

# Add these helper functions if they're not already in your app.py
def get_meal_categories(pre_meal):
    if pre_meal.lower() == 'vegetarian':
        return {
            'Breakfast': ['Breakfast grains', 'Fruits', 'Vegetables', 'Protein', 'Healthy Fats', 'Breads', 'Juice', 'Indian bread', 'Tea & Coffee'],
            'Lunch': ['Grains', 'Indian bread', 'Vegetables', 'Salads', 'Healthy Fats', 'Soup', 'Dairy'],
            'Snacks': ['Tea & Coffee', 'Sandwich', 'Nuts & Seeds', 'Fruits', 'Beverages', 'Juice'],
            'Dinner': ['Grains', 'Indian bread', 'Vegetables', 'Salads', 'Healthy Fats', 'Soup', 'Dairy']
        }
    elif pre_meal.lower() == 'non-vegetarian':
        return {
            'Breakfast': ['Breakfast grains', 'Fruits', 'Vegetables', 'Non-veg Protein', 'Protein', 'Healthy Fats', 'Breads', 'Juice', 'Indian bread', 'Tea & Coffee'],
            'Lunch': ['Grains', 'Indian bread', 'Vegetables', 'Salads', 'Healthy Fats', 'Soup', 'Dairy', 'Meat', 'Non-veg Salads', 'Non-veg Soup'],
            'Snacks': ['Tea & Coffee', 'Sandwich', 'Nuts & Seeds', 'Fruits', 'Beverages', 'Juice', 'Non-veg Sandwich'],
            'Dinner': ['Grains', 'Indian bread', 'Vegetables', 'Salads', 'Healthy Fats', 'Soup', 'Dairy', 'Meat', 'Non-veg Salads', 'Non-veg Soup']
        }
    else:
        return {}

def get_random_dish(meal_category, pre_meal):
    meal_categories = get_meal_categories(pre_meal)
    if meal_category in meal_categories:
        return random.choice(meal_categories[meal_category])
    return 'No Dish'

def generate_weekly_diet_chart(pre_meal):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    table = []
    for day in days_of_week:
        row = [day]
        for meal in ['Breakfast', 'Lunch', 'Snacks', 'Dinner']:
            random_dish = get_random_dish(meal, pre_meal)
            row.append(random_dish)
        table.append(row)
    return table



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
