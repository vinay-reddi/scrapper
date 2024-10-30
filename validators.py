import requests
# import spacy
from bs4 import BeautifulSoup
from textblob import TextBlob
import numpy as np
from datetime import datetime

# nlp = spacy.load("en_core_web_sm")

def domain_reputation(url):
    api_key = "AIzaSyCuthoIoEUFRGLrwyFfMdxJKziqL7eBVRI"
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
    body = {
        "client": {
            "clientId": "yourcompany",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    response = requests.post(api_url, json=body)
    if response.status_code == 200 and "matches" not in response.json():
        return 1.0
    return 0.0

def data_freshness(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if 'date' in tag.attrs.get('name', '').lower() or 'date' in tag.attrs.get('property', '').lower():
                date_str = tag.attrs.get('content')
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                age_in_days = (datetime.now() - date_obj).days
                return 1.0 if age_in_days < 365 else 0.0
    except Exception:
        pass
    return 0.0

def content_quality(url):
    try:
        response = requests.get(url)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # text = soup.get_text()
        # doc = nlp(text)
        # sentences = list(doc.sents)
        # if len(sentences) < 5:
        #     return 0.0
        # blob = TextBlob(text)
        # readability_score = blob.sentiment.polarity
        # return min(max(readability_score, 0.0), 1.0)
        return 0.25
    except Exception:
        return 0.0

def content_relevance(url, keyword):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        documents = [text, keyword]
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer().fit_transform(documents)
        vectors = vectorizer.toarray()
        cosine_similarity = np.dot(vectors[0], vectors[1]) / (np.linalg.norm(vectors[0]) * np.linalg.norm(vectors[1]))
        return cosine_similarity
    except Exception:
        return 0.0

def calculate_final_score(domain_reputation_score, data_freshness_score, content_quality_score, 
                          source_redundancy_score, author_credibility_score, content_relevance_score,
                          originality_score):
    return round((0.25 * domain_reputation_score +
            0.15 * data_freshness_score +
            0.2 * content_quality_score +
            0.15 * source_redundancy_score +
            0.1 * author_credibility_score +
            0.1 * content_relevance_score +
            0.05 * originality_score)*300,2)
