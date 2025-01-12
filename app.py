from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Load mock data
def load_data():
    with open('data.json') as f:
        return json.load(f)

mock_data = load_data()

@app.route('/')
def home():
    return render_template('home.html', data=mock_data)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    location = request.form.get('location')
    farming_type = request.form.get('farming_type')
    region_data = mock_data.get(location)

    if not region_data:
        return render_template(
            'home.html',
            error=f"No data available for '{location}'. Please try another location.",
            data=mock_data
        )

    farming_data = region_data.get('farming', {}).get(farming_type)
    if not farming_data:
        return render_template(
            'recommendations.html',
            location=location,
            farming_type=farming_type,
            error=f"No recommendations available for {farming_type} farming in this location.",
            data=region_data
        )

    return render_template('recommendations.html', location=location, farming_type=farming_type, data=farming_data)

@app.route('/markets')
def markets():
    try:
        markets_data = mock_data.get('markets', [])
        return render_template('markets.html', data=markets_data)
    except KeyError:
        return render_template('error.html', message="Markets data not found.")

@app.route('/news')
def news():
    try:
        news_data = mock_data.get('news', [])
        return render_template('news.html', data=news_data)
    except KeyError:
        return render_template('error.html', message="News data not found.")

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    article = next((item for item in mock_data['news'] if item['id'] == news_id), None)
    if not article:
        return render_template('error.html', message="News article not found.")
    return render_template('news_detail.html', article=article)

@app.route('/services')
def services():
    try:
        services_data = mock_data.get('services', [])
        return render_template('services.html', data=services_data)
    except KeyError:
        return render_template('error.html', message="Services data not found.")

@app.route('/blogs')
def blogs():
    return render_template('blogs.html', blogs=mock_data['blogs'])

@app.route('/blogs/<int:blog_id>')
def blog_detail(blog_id):
    blog = next((item for item in mock_data['blogs'] if item['id'] == blog_id), None)
    if not blog:
        return render_template('error.html', message="Blog not found.")
    return render_template('blog_detail.html', blog=blog)

@app.route('/blogs/post', methods=['GET', 'POST'])
def blog_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_blog = {
            "id": len(mock_data['blogs']) + 1,
            "title": title,
            "content": content,
            "image": "blog2.jpg"  # Placeholder image for new blogs
        }
        mock_data['blogs'].append(new_blog)
        return redirect(url_for('blogs'))
    return render_template('blog_post.html')

@app.route('/marketplace')
def marketplace():
    categories = mock_data['marketplace_categories']
    return render_template('marketplace.html', categories=categories)

@app.route('/marketplace/post', methods=['GET', 'POST'])
def post_item():
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        contact = request.form['contact']
        image = "placeholder.jpg"  # Use a default placeholder image

        new_item = {
            "category": category,
            "name": name,
            "description": description,
            "price": price,
            "contact": contact,
            "image": image
        }
        mock_data['marketplace_categories'][category].append(new_item)
        return redirect(url_for('marketplace'))

    return render_template('post_item.html')


@app.route('/loans')
def loans():
    return render_template('loans.html')
import requests

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        location = request.form.get('location')
        api_key = "73b8d78452ec054753f7274f8f578e73"  # Your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for HTTP errors

            data = response.json()

            if data.get("cod") == 200:  # Successful response
                weather_data = {
                    "location": data.get("name"),
                    "temperature": data["main"].get("temp"),
                    "condition": data["weather"][0].get("description", "").capitalize(),
                    "humidity": data["main"].get("humidity")
                }
            else:
                error_message = f"Weather data not found for '{location}'. Please check the location name."
        except requests.exceptions.RequestException:
            error_message = "An error occurred while fetching the weather data. Please try again later."

    return render_template('weather.html', weather_data=weather_data, error_message=error_message)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chatbot')
def chatbot():
    return jsonify({"response": "Hello! How can I assist you today?"})
# Mock remote sensing data
remote_sensing_data = {
    "Gaborone": {"soil_moisture": "Low", "pest_risk": "High", "advice": "Irrigation recommended. Apply pesticides."},
    "Francistown": {"soil_moisture": "Moderate", "pest_risk": "Low", "advice": "No immediate action needed."},
    "Maun": {"soil_moisture": "High", "pest_risk": "Medium", "advice": "Monitor for waterlogging and pests."},
    "Kasane": {"soil_moisture": "Low", "pest_risk": "Medium", "advice": "Consider drip irrigation and pest monitoring."},
    "Palapye": {"soil_moisture": "Moderate", "pest_risk": "High", "advice": "Apply organic mulch and insect repellents."}
}




@app.route('/calculate-loan', methods=['POST'])
def calculate_loan():
    try:
        loan_amount = float(request.form.get('loan_amount'))
        interest_rate = float(request.form.get('interest_rate')) / 100
        years = int(request.form.get('years'))

        # Loan calculation
        monthly_rate = interest_rate / 12
        months = years * 12
        monthly_payment = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)
        total_payment = monthly_payment * months

        return render_template(
            'loan_result.html',
            loan_amount=loan_amount,
            interest_rate=interest_rate * 100,
            years=years,
            monthly_payment=round(monthly_payment, 2),
            total_payment=round(total_payment, 2),
        )
    except Exception as e:
        return f"Error: {e}", 400
livestock_data = []  # For storing livestock records
input_data = []      # For storing BAMB input records


# Mock data for Livestock and BAMB tools
livestock_data = []
input_data = []

# Load Market Insights data
try:
    with open('market_data.json', 'r') as file:
        market_data = json.load(file)
except FileNotFoundError:
    market_data = {}  # Default to empty if the file is missing

# Feedback Data
feedback_data = []

# Consultancy Page
@app.route('/consultancy', methods=['GET', 'POST'])
def consultancy():
    return render_template(
        'consultancy.html',
        livestock_data=livestock_data,
        input_data=input_data,
        market_data=market_data,
        feedback_data=feedback_data,
        data=None  # For Remote Sensing section
    )

# Livestock Management
@app.route('/livestock', methods=['POST'])
def livestock():
    animal_type = request.form.get('animal_type')
    quantity = int(request.form.get('quantity'))
    health_status = request.form.get('health_status')
    livestock_data.append({
        "animal_type": animal_type,
        "quantity": quantity,
        "health_status": health_status
    })
    return redirect(url_for('consultancy'))

# BAMB Input Tracking
@app.route('/bamb', methods=['POST'])
def bamb():
    input_type = request.form.get('input_type')
    quantity_used = int(request.form.get('quantity_used'))
    crop_yield = int(request.form.get('crop_yield'))
    input_data.append({
        "input_type": input_type,
        "quantity_used": quantity_used,
        "crop_yield": crop_yield
    })
    return redirect(url_for('consultancy'))

# Remote Sensing
@app.route('/remote-sensing', methods=['POST'])
def remote_sensing():
    location = request.form.get('location')
    # Mock data for Remote Sensing
    remote_data = {
        "soil_moisture": "High",
        "pest_risk": "Low",
        "irrigation_advice": "Water every 5 days"
    }
    return render_template(
        'consultancy.html',
        livestock_data=livestock_data,
        input_data=input_data,
        market_data=market_data,
        feedback_data=feedback_data,
        data=remote_data,
        location=location
    )

# Feedback Mechanism
@app.route('/feedback', methods=['POST'])
def feedback():
    name = request.form.get('name')
    message = request.form.get('message')
    feedback_data.append({
        "name": name,
        "message": message
    })
    return redirect(url_for('consultancy'))







# Buyer Request Route
buyer_requests = []


@app.route('/marketplace/request', methods=['POST'])
def marketplace_request():
    # Gather form data
    item = request.form['item']
    location = request.form['location']
    contact = request.form['contact']

    # Create a new buyer request
    new_request = {
        "item": item,
        "location": location,
        "contact": contact
    }

    # Add the request to mock_data
    if 'buyer_requests' not in mock_data:
        mock_data['buyer_requests'] = []
    mock_data['buyer_requests'].append(new_request)

    # Redirect with a confirmation message
    message = "Your request has been submitted. Sellers will contact you soon!"
    categories = mock_data['marketplace_categories']
    return render_template('marketplace.html', categories=categories, buyer_requests=mock_data['buyer_requests'], message=message)

# Mock user database (replace with a real database later)
user_database = []

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user already exists
        for user in user_database:
            if user['email'] == email:
                return "User already exists!", 400

        # Save the user data
        user_database.append({"name": name, "email": email, "password": password})
        return redirect(url_for('home'))  # Redirect to home after successful registration

    return render_template('signup.html')









if __name__ == '__main__':
    app.run()
