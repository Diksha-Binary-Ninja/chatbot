from flask import Flask, render_template, request, jsonify, redirect
import requests
from bs4 import BeautifulSoup
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

app = Flask(__name__)
openai.api_key = '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'
messages = []  # Initialize the messages list
chromedriver_path = r'C:\Users\nkoni\OneDrive\chromedriver.exe'  # Update this with your actual path


def get_weather(city):
    base_url = f'https://www.weather-forecast.com/locations/{city}/forecasts/latest'
    response = requests.get(base_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        weather_info = soup.find(class_='b-forecast__table-description-content').get_text(strip=True)
        return f"Weather in {city}: {weather_info}"
    else:
        return "City Not Found."



@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    global messages
    user_message = request.form['user_input']
    if user_message:
        messages.append({"role": "user", "content": user_message})

        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})

        return jsonify({"role": "assistant", "content": reply})

@app.route('/get_weather', methods=['POST'])
def get_city_weather():
    city = request.form['city']
    weather_info = get_weather(city)
    return jsonify({"role": "assistant", "content": weather_info})

@app.route('/market_price', methods=['GET'])
def market_price():
    # Redirect to the desired URL when the Market Price link is clicked
    return redirect('https://enam.gov.in/web/dashboard/trade-data')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
