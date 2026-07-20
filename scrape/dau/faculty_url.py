import requests
from bs4 import BeautifulSoup

def facultyUrls(url, verbose=False):
    try:

        html = requests.get(url).text
        
        soup = BeautifulSoup(html, "html.parser")

        cards = soup.select("div.personalDetails, div.personalDetail, div.personalsDetails, div.personalDetailsGer,div.personalDetails div.personalDetailsGer")
        
        faculty_urls = [
            card.find("a")["href"]
            for card in cards
            if card.find("a") and card.find("a").get("href")
        ]
        
        if verbose:
            print(f'Url: {url} \n Number of Urls Extracted: {len(faculty_urls)} \n')

        return faculty_urls

    except Exception as e:
        print(e)
