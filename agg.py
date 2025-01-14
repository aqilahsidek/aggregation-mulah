import requests
import json
import datetime
from bs4 import BeautifulSoup

def monthly():
    urls = []
    start = datetime.date(2022,1,1)
    end = datetime.date.today()

    while start <= end:
        urls.append(f"https://www.theverge.com/archives/{start.year}/{start.month}")
        if start.month == 12:
            start = datetime.date(start.year +1, 1, 1)
        else:
            start = datetime.date(start.year, start.month+1, 1)

    return urls

def scrape():
    articles = []
    url_month = monthly()

    for url in url_month:
        reqs = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if reqs.status_code != 200:
            print(f"Failed to fetch {url}")
            continue

        soup = BeautifulSoup(reqs.text, 'html.parser')

        for element in soup.select(".c-entry-box--compact__body"):
            titleT = element.select_one(".c-entry-box--compact__title")
            linkT = element.select_one("a")
            dateT = element.select_one("time")

            if titleT and linkT:
                articles.append({
                    "title": titleT.get_text(strip=True),
                    "url": linkT["href"],
                    "date": dateT["datetime"] if dateT else None
                })
        
        articles.sort(key=lambda x: x["date"], reverse=True)

        with open("theTitle.json", "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=2)

        html_content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width initial-scale=1">

            <style>
                body{{
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    width: 100%;
                }}

                h1{{
                    font-size:50px;
                }}

                .article a{{
                    font-family: Arial;
                    line-height: 2;
                    color: black;
                    text-decoration: none;
                }}

                .article a:hover{{
                    color: blue;
                    text-decoration: underline;
                }}

            </style>
            <title>Articles</title>
        </head>
        <body>
            <h1>The Verge Articles</h1>
            {''.join([f'<div class="article"><a href="{a["url"]}">{a["title"]}</a></div>'for a in articles])}
        </body>
        </html>
        """

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

scrape()
