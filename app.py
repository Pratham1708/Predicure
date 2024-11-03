from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
import pandas as pd
import random
import os

app = Flask(__name__)
CORS(app)

# Load models and data
try:
    model = pickle.load(open('model.pkl', 'rb'))
    model_1 = pickle.load(open('model_100.pkl', 'rb'))
    food = pd.read_csv('final_food_items.csv')
    calorie = pd.read_csv('Calorie_value.csv')
    diseases_data = pd.read_csv('diseases.csv')
except Exception as e:
    print(f"Error loading models or data: {str(e)}")

# Utility functions
def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate"""
    try:
        if gender.lower() == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        elif gender.lower() == 'female':
            return 10 * weight + 6.25 * height - 5 * age - 161
        else:
            raise ValueError("Invalid gender specified")
    except Exception as e:
        print(f"Error calculating BMR: {str(e)}")
        return None

def calculate_calories(bmr, activity_level):
    """Calculate daily calorie requirements"""
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly': 1.375,
        'moderately': 1.55,
        'active': 1.725,
        'extra': 1.9
    }
    
    try:
        activity = activity_level.lower()
        if activity in activity_multipliers:
            return bmr * activity_multipliers[activity]
        else:
            raise ValueError("Invalid activity level specified")
    except Exception as e:
        print(f"Error calculating calories: {str(e)}")
        return None

def get_meal_categories(pre_meal):
    """Get meal categories based on dietary preference"""
    if pre_meal.lower() == 'vegetarian':
        return {
            'Breakfast': ['Oatmeal', 'Fruits', 'Vegetables', 'Tofu', 'Nuts', 'Whole Grain Bread', 'Fresh Juice', 'Roti', 'Green Tea'],
            'Lunch': ['Brown Rice', 'Chapati', 'Mixed Vegetables', 'Green Salad', 'Avocado', 'Vegetable Soup', 'Yogurt'],
            'Snacks': ['Herbal Tea', 'Veggie Sandwich', 'Mixed Nuts', 'Fresh Fruits', 'Smoothie', 'Fresh Juice'],
            'Dinner': ['Quinoa', 'Roti', 'Steamed Vegetables', 'Sprout Salad', 'Olive Oil', 'Lentil Soup', 'Cottage Cheese']
        }
    elif pre_meal.lower() == 'non-vegetarian':
        return {
            'Breakfast': ['Eggs', 'Fruits', 'Vegetables', 'Chicken', 'Fish', 'Nuts', 'Whole Grain Bread', 'Fresh Juice', 'Roti', 'Coffee'],
            'Lunch': ['Brown Rice', 'Chapati', 'Vegetables', 'Salad', 'Olive Oil', 'Soup', 'Yogurt', 'Grilled Chicken', 'Tuna Salad', 'Chicken Soup'],
            'Snacks': ['Tea', 'Chicken Sandwich', 'Nuts', 'Fruits', 'Protein Shake', 'Juice', 'Egg Sandwich'],
            'Dinner': ['Quinoa', 'Roti', 'Vegetables', 'Salad', 'Avocado', 'Soup', 'Yogurt', 'Fish', 'Chicken Salad', 'Meat Soup']
        }
    return {}

def generate_weekly_diet_chart(pre_meal):
    """Generate weekly diet chart"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    meals = ['Breakfast', 'Lunch', 'Snacks', 'Dinner']
    meal_categories = get_meal_categories(pre_meal)
    
    weekly_chart = []
    for day in days:
        day_meals = [day]
        for meal in meals:
            if meal in meal_categories:
                day_meals.append(random.choice(meal_categories[meal]))
            else:
                day_meals.append('Meal not specified')
        weekly_chart.append(day_meals)
    
    return weekly_chart

# Route handlers
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/<path:filename>')
def serve_pages(filename):
    if filename.endswith('.html'):
        return render_template(filename)
    return "Page not found", 404

@app.route('/submit_1', methods=['POST'])
def submit_1():
    try:
        int_features = [float(x) for x in request.form.values()]
        final_features = [np.array(int_features)]
        prediction = model_1.predict(final_features)

        output = int(prediction[0])
        result_map = {
            0: "Insufficient_Weight",
            1: "Normal Weight",
            2: "Overweight Level I",
            3: "Overweight Level II",
            4: "Obesity Type I",
            5: "Obesity Type II",
            6: "Obesity Type III"
        }
        
        output = result_map.get(output, "Unknown Category")
        return render_template('obesity_form.html', prediction_text=f'You are most probably {output}')
    except Exception as e:
        return render_template('obesity_form.html', prediction_text=f'Error: {str(e)}')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        int_features = [float(x) for x in request.form.values()]
        final_features = [np.array(int_features)]
        prediction = model.predict(final_features)

        output = "Diabetic" if prediction[0] == 1 else "Non diabetic"
        return render_template('diabetes_form.html', prediction_text=f'You are mostly likely to be {output}')
    except Exception as e:
        return render_template('diabetes_form.html', prediction_text=f'Error: {str(e)}')

@app.route('/recommendation', methods=['POST'])
def recommendation():
    try:
        data = request.json
        print("Received data:", data)  # Debug print

        # Extract and validate input
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
            return jsonify({'error': 'Invalid input for BMR calculation'}), 400

        calories = calculate_calories(bmr, activity_level)
        if calories is None:
            return jsonify({'error': 'Invalid input for calorie calculation'}), 400

        # Generate diet charts
        weekly_diet_charts = []
        for _ in range(3):  # Generate 3 weeks of diet charts
            weekly_diet_charts.append(generate_weekly_diet_chart(pre_meal))

        # Prepare response
        response_data = {
            'bmr': bmr,
            'calories': calories,
            'weekly_diet_charts': weekly_diet_charts
        }

        return jsonify(response_data)

    except Exception as e: # Catch-all for unexpected errors
        print(f"Error during recommendation: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
