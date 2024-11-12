import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def formSearch():
    return render_template("search.html")

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    results = []
    for page in range(1, 4):  # Loop through the first 3 pages
        url = f'https://www.detik.com/search/searchall?query={query}&page={page}'

        # Handle network-related errors
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an error for HTTP errors
        except requests.exceptions.RequestException as e:
            # This handles network issues, timeout, and other request errors
            return jsonify({"error": "Network error", "details": str(e)}), 503

        # Check if response content is valid HTML
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            return jsonify({"error": "Failed to parse HTML", "details": str(e)}), 500
        
        # Check if articles are present on the page
        articles = soup.find_all('article')  # Adjust the element and class if needed
        if not articles:
            return jsonify({"message": "No articles found"}), 404

        # Extract details for each article
        for article in articles:
            try:
                title_tag = article.find('h3')
                image_tag = article.find('img')
                body_tag = article.find('div', class_='media__desc')
                time_tag = article.find('div', class_='media__date')
                time_span = time_tag.find('span') if time_tag else None

                # Extracting data with error handling for missing data
                title = title_tag.get_text(strip=True) if title_tag else "No title"
                link = article.find('a')['href'] if article.find('a') else ""
                image_link = image_tag['src'] if image_tag else ""
                body_text = body_tag.get_text(strip=True) if body_tag else "No content"
                publication_time = time_span['title'] if time_span and 'title' in time_span.attrs else "No time"

                results.append({
                    "title": title,
                    "link": link,
                    "image_link": image_link,
                    "body_text": body_text,
                    "publication_time": publication_time
                })
            except AttributeError as e:
                # If there is any missing data in the article structure
                continue  # Skip this article if it has missing fields

    if not results:
        return jsonify({"message": "No results found"}), 404

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)





