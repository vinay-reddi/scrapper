
import requests

def scrape_keyword(keyword, num_results=50):
    api_key = "AIzaSyCuthoIoEUFRGLrwyFfMdxJKziqL7eBVRI"  
    cse_id = "407e0cfb802304419"    

    results = []
    start_index = 1

    while len(results) < num_results and start_index <= 91:
        url = f"https://www.googleapis.com/customsearch/v1?q={keyword}&key={api_key}&cx={cse_id}&start={start_index}"
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return [{"title": "Error", "link": "N/A", "description": "Failed to retrieve data"}]

        data = response.json()
        items = data.get('items', [])
        
        if not items:
            break

        for item in items:
            title = item.get('title', 'No Title')
            link = item.get('link', 'No Link')
            description = item.get('snippet', 'No Description')
            
            results.append({
                "title": title,
                "link": link,
                "description": description
            })
            
            if len(results) >= num_results:
                break

        start_index += 10

    print(f"Total results retrieved: {len(results)}")
    return results