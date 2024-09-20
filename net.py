from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# Function to scrape news from stockanalysis.com
def scrape_news():
    url = 'https://stockanalysis.com/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all relevant divs for news articles
    divs = soup.find_all('div', class_='rounded border border-gray-200 p-4 text-sm dark:border-dark-700')

    news_list = []  # List to store the news items

    # Loop through each div and extract relevant information
    for div in divs:
        div_text = div.text.strip()  # Headline or main content of the div

        # Find the unordered lists within the div (if available)
        uls = div.find_all('ul', class_='text-gray-700 dark:text-dark-300')

        # Loop through each ul and extract the li content
        for ul in uls:
            li_content = ul.text.strip()  # Extracting the details in the list

            # Append the scraped data to the news list
            news_list.append({
                'headline': div_text,
                'details': li_content
            })

    return news_list  # Return the list of news

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Finance News API!"})

# News scraping route
@app.route('/news', methods=['GET'])
def get_news():
    try:
        news = scrape_news()  # Scrape the news
        return jsonify({
            'status': 'success',
            'news': news
        }), 200  # Return scraped news with a success status
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  # Return an error message if scraping fails

# Main entry point to run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)















































