from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure SQLite database
DATABASE = 'database.db'


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT,
            password TEXT
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS dit_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                height INTEGER,
                weight INTEGER,
                gender TEXT,
                ActivityLevel TEXT,  
                Weightplan TEXT,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dash (
        id INTEGER PRIMARY KEY,
        name text,
        calories number,
        carbs number,
        protein number
    )
''')
    

    conn.commit()
    conn.close()

create_table()
#@app.route('/')
#def index():
 #   return render_template('hopa.html')
# Load your dataset of recipes

data = pd.read_csv(r'C:\flaskweb\flaskweb\Calories.csv')


def calculate_bmr(age, height, weight, gender):
    if gender == "Male":
        bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
    else:  # Female
        bmr = 655.1 + (9.563 * weight) + (1.85 * height) - (4.676 * age)
    return bmr

def adjust_bmr_for_activity(bmr, activity_level):
    activity_multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (light exercise/sports 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise/sports 3-5 days/week)": 1.55,
        "Very active (hard exercise/sports 6-7 days a week)": 1.725,
        "Super active (very hard exercise/sports & a physical job)": 1.9
    }
    return bmr * activity_multipliers[activity_level]

def apply_weight_plan(maintenance_calories, weight_plan):
    weight_plan_multipliers = {
        "Maintain weight": 1,
        "Mild weight loss": 0.9,
        "Weight loss": 0.8,
        "Extreme weight loss": 0.6,
        "Mild weight gain": 1.1,
        "Weight gain": 1.2,
        "Rapid weight gain": 1.3
    }
    return round(maintenance_calories * weight_plan_multipliers[weight_plan],2)

def calculate_macronutrients(caloric_needs):
    protein_grams = (0.10 * caloric_needs) / 4
    carbs_grams = (0.55 * caloric_needs) / 4
    fats_grams = (0.30 * caloric_needs) / 9
    fiber_grams = (caloric_needs / 1000) * 14
    return protein_grams, carbs_grams, fats_grams, fiber_grams
   
    print("\nBased on your inputs, here are your nutritional needs:")
    print(f"Caloric needs: {final_caloric_needs} kcal/day")
    print(f"Protein: {protein}g")
    print(f"Carbohydrates: {carbs}g")
    print(f"Fats: {fats}g")
    print(f"Fiber: {fiber}g")
    return final_caloric_needs, protein, carbs, fats, fiber

def recommend_recipes(user_caloric_needs, pipeline, user_nutritional_needs, data):
    total_calories = 0
    recommended_indices_list = []
    neighbors_to_consider = 8  # Start with 10 neighbors

    while total_calories < user_caloric_needs and neighbors_to_consider <= data.shape[0]:
        # Update the pipeline to consider more neighbors
        pipeline.set_params(NN__kw_args={'n_neighbors': neighbors_to_consider, 'return_distance': False})

        # Get recommended indices
        recommended_indices = pipeline.transform(user_nutritional_needs)[0]

        for index in recommended_indices:
            if index not in recommended_indices_list:  # Avoid adding the same recipe multiple times
                recipe = data.iloc[index]
                total_calories += recipe['Calories']
                recommended_indices_list.append(index)

                if total_calories >= user_caloric_needs:
                    return data.iloc[recommended_indices_list]

        # If we haven't met the caloric needs, consider more neighbors in the next iteration
        neighbors_to_consider += 8

    return data.iloc[recommended_indices_list]


@app.route('/')
def registration_page():
    return render_template('register.html')

@app.route('/', methods=['POST'])
def register():
    name = request.form['Name']
    username = request.form['Username']
    password = request.form['Password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, username, password) VALUES (?, ?, ?)', (name, username, password))
    conn.commit()
    conn.close()
    flash('Registration successful!', 'success')
    return redirect(url_for('login'))

@app.route('/login.html')
def login_page():
   return render_template('login.html')

@app.route('/login.html', methods=['POST'])
def login():
    username = request.form['Username']
    password = request.form['Password']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Successful login, you can add session handling or redirect to a user dashboard.
        flash('Login successful!', 'success')
        return redirect(url_for('ui'))
    else:
        # Incorrect username or password, you may want to display an error message.
        flash('Login failed. Please check your username and password.', 'danger')
        return redirect(url_for('login'))

#@app.route('/ui.html')
#def ui():
    #return render_template('ui.html')

@app.route('/diet.html', methods=['POST', 'GET'])
def diet():
    if request.method == 'POST':
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        gender = request.form['gender']
        activity_level = request.form['activity_level']
        weight_plan = request.form['weight_plan']

        bmr = calculate_bmr(age, height, weight, gender)
        maintenance_calories = adjust_bmr_for_activity(bmr, activity_level)
        final_caloric_needs = apply_weight_plan(maintenance_calories, weight_plan)
         # Print statement to verify caloric needs
        print(f"Caloric needs: {final_caloric_needs}")
        user_nutritional_needs = np.array([calculate_macronutrients(final_caloric_needs)])
        daily_protein, daily_carbohydrates, daily_fats, daily_fiber = calculate_macronutrients(final_caloric_needs) 
        # Filter recipes based on nutritional criteria
        max_Calories = final_caloric_needs
        max_daily_fat = final_caloric_needs * 0.30 / 9
        max_daily_Saturatedfat = 13
        max_daily_Cholesterol = 300
        max_daily_Sodium = 2300
        max_daily_Carbohydrate = final_caloric_needs * 0.55 / 4
        max_daily_Fiber = final_caloric_needs / 1000 * 14
        max_daily_Sugar = 40
        max_daily_Protein = final_caloric_needs * 0.10 / 4

        max_list = [max_Calories, max_daily_fat, max_daily_Saturatedfat, max_daily_Cholesterol, max_daily_Sodium,
                    max_daily_Carbohydrate, max_daily_Fiber, max_daily_Sugar, max_daily_Protein]

        extracted_data = data.copy()
        relevant_columns = [4,5,6,7,9]
        for column, maximum in zip(extracted_data.columns[relevant_columns], max_list):
            extracted_data = extracted_data[extracted_data[column] < maximum]

        # Standardize the nutritional data
        scaler = StandardScaler()
        prep_data = scaler.fit_transform(extracted_data.iloc[:, relevant_columns].to_numpy())

        neigh = NearestNeighbors(metric='cosine', algorithm='brute')
        neigh.fit(prep_data)

        transformer = FunctionTransformer(neigh.kneighbors, kw_args={'return_distance': False})
        pipeline = Pipeline([('std_scaler', scaler), ('NN', transformer)])

        params = {'n_neighbors': 8, 'return_distance': False}
        pipeline.set_params(NN__kw_args=params)

        daily_calories = final_caloric_needs
        

        user_nutritional_needs = np.array([[daily_calories, daily_fats, daily_carbohydrates, daily_fiber, daily_protein]])
        recommended_recipes = recommend_recipes(final_caloric_needs, pipeline, user_nutritional_needs, extracted_data)

        #return render_template('diet.html', recommended_recipes=recommended_recipes)
        return render_template('diet.html', recommended_recipes=recommended_recipes, final_caloric_needs=final_caloric_needs)
    



    return render_template('diet.html', recommended_recipes=None)
    
@app.route('/dash.html')
def index():
     if request.method == 'POST':
        meal = request.form['meal']
        name = request.form['name']
        calories = request.form['calories']
        carbs = request.form['carbs']
        protein = request.form['protein']

        # Perform the database insertion
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Perform the database insertion
        cursor.execute("INSERT INTO dash (name, calories, carbs, protein) VALUES (?, ?, ?, ?)",
                       (name, calories, carbs, protein))
        conn.commit()
        conn.close()
     return render_template('dash.html')




@app.route('/BMI.html', endpoint='bmi_calculator')
def index():
    return render_template('BMI.html')




if __name__ == '__main__':
    app.run(debug=True)