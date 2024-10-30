from flask import Flask, render_template, request
from scraper import scrape_keyword
from validators import domain_reputation, data_freshness, content_quality, content_relevance, calculate_final_score
import subprocess
# import spacy


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword')
    num_results = request.form.get('num')
    results = scrape_keyword(keyword, int(num_results))

    for result in results:
        url = result['link']
        domain_reputation_score = domain_reputation(url)
        data_freshness_score = data_freshness(url)
        content_quality_score = content_quality(url)
        content_relevance_score = content_relevance(url, keyword)

        source_redundancy_score = 0.8
        author_credibility_score = 0.7
        originality_score = 0.9
        print( domain_reputation_score, data_freshness_score, content_quality_score,
            source_redundancy_score, author_credibility_score, content_relevance_score,
            originality_score)
        final_score = calculate_final_score(
            domain_reputation_score, data_freshness_score, content_quality_score,
            source_redundancy_score, author_credibility_score, content_relevance_score,
            originality_score
        )

        result['validation'] = {
            'final_score': final_score
        }

    return render_template('results.html', keyword=keyword, results=results)

if __name__ == '__main__':
    app.run(debug=True)
