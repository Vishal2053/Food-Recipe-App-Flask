from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your Spoonacular API key
API_KEY = 'YOUR_API_KEY'
BASE_URL = 'https://api.spoonacular.com/recipes/complexSearch'
RECIPE_URL = 'https://api.spoonacular.com/recipes/{id}/information'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    recipe_name = request.form['recipe_name']
    if not recipe_name:
        return render_template('home.html', error="Please enter a recipe name.")

    # Fetch recipes matching the name
    params = {
        'query': recipe_name,
        'number': 1,  # Only get the top result
        'apiKey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return render_template('home.html', error="Error fetching data from API.")
    
    data = response.json()
    if not data.get('results'):
        return render_template('home.html', error="Recipe not found.")

    # Get the first recipe ID
    recipe_id = data['results'][0]['id']

    # Fetch detailed recipe information
    detailed_response = requests.get(RECIPE_URL.format(id=recipe_id), params={'apiKey': API_KEY})
    if detailed_response.status_code != 200:
        return render_template('home.html', error="Error fetching recipe details.")

    detailed_data = detailed_response.json()

    # Extract the required details
    title = detailed_data.get('title', 'Recipe')
    image = detailed_data.get('image')
    ingredients = [ingredient['original'] for ingredient in detailed_data.get('extendedIngredients', [])]
    instructions = detailed_data.get('instructions', 'No instructions available').split('. ')

    return render_template('recipe.html', title=title, image=image, ingredients=ingredients, instructions=instructions)

if __name__ == '__main__':
    app.run(debug=True)
