from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

def scrape_news():
    url = 'https://stockanalysis.com/news/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    divs = soup.find_all('div', class_='rounded border border-gray-200 p-4 text-sm dark:border-dark-700')

    news_list = []  


    for div in divs:
        div_text = div.text.strip()  
        uls = div.find_all('ul', class_='text-gray-700 dark:text-dark-300')
        
        for ul in uls:
            li_content = ul.text.strip() 
            news_list.append({
                'headline': div_text,
                'details': li_content
            })
    
    return news_list


@app.route('/news', methods=['GET'])
def get_news():
    try:
        news = scrape_news()  
        return jsonify({
            'status': 'success',
            'news': news
        }), 200  
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)

