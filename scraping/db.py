from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

try:
    response = requests.get("https://www.digitaltrends.com/movies/best-movies-on-netflix/")
    soup = BeautifulSoup(response.text, 'html.parser')

    article = soup.find('article', class_='b-content b-single__content h-article-content b-content--best-of')
    article_list={"article_name":[], "article_director": []}
    if article:
        article_name = article.find_all("h3", class_="b-media__title")
        article_director = article.find_all("span", class_="dt-clamp dt-clamp-1")
       
        for name, director in zip(article_name,article_director):
            # Extract and clean the movie title text
            article_name = name.get_text(strip=True).replace('(',"")
            article_name = article_name.replace(')',"")
            article_director = director.get_text(strip=True)

            article_list["article_name"].append(article_name) 
            article_list["article_director"].append(article_director)

    else:
        print("Article not found. Check the page structure.")
except Exception as e:
    print(e)

df=pd.DataFrame(data=article_list)
print(df.head())

connection=sqlite3.connect("test.db")
cursor=connection.cursor()
query="create table if not exists movie(article_name,article_director)"
cursor.execute(query)
for i in range(len(df)):
    row = df.iloc[i]
    cursor.execute("INSERT INTO movie VALUES (?, ?)", (row['article_name'], row['article_director']))

connection.commit()
connection.close()