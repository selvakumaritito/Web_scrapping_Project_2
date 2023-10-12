from bs4 import BeautifulSoup
import requests, openpyxl

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title="Movie List"
sheet.append(['Movie Name', 'Director'])

try:
    response = requests.get("https://www.digitaltrends.com/movies/best-movies-on-netflix/")
    soup = BeautifulSoup(response.text, 'html.parser')

    article = soup.find('article', class_='b-content b-single__content h-article-content b-content--best-of')

    if article:
        article_name = article.find_all("h3", class_="b-media__title")
        article_director = article.find_all("span", class_="dt-clamp dt-clamp-1")
        #article_Genre=  article.find_all("span", class_="dt-clamp dt-clamp-2")
        #article_rate = article.find_all("div", class_="b-media__rating-score")
        for name, director in zip(article_name,article_director):
            # Extract and clean the movie title text
            article_name = name.get_text(strip=True).replace('(',"")
            article_name = article_name.replace(')',"")
            
            article_director = director.get_text(strip=True)
                   
            #article_rate = rate.get_text(strip=True)
            #article_Genre = Genre.get_text(strip=True)


            #print(f"{article_name} {article_director}{article_Genre}")   

            #print(f"{article_name} {article_director}") 
            sheet.append([article_name, article_director])  

    else:
        print("Article not found. Check the page structure.")
except Exception as e:
    print(e)

excel.save("Movies.xlsx")