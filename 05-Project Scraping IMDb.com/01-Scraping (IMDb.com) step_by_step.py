import pandas as pd
from bs4 import BeautifulSoup
from requests import get


url = "https://www.imdb.com/search/title/?release_date=2017&sort=num_votes,desc&page=1"

response = get(url).content
html_soup = BeautifulSoup(response, 'html.parser')
# print(html_soup.prettify())

movie_containers = html_soup.find_all("div", class_="lister-item mode-advanced")
# print(f'type = {type(movie_containers)}, length = {len(movie_containers)}')

# ------ Extract Data for One Film ------

first_name = movie_containers[0].h3.a.text
# print(first_name)

first_year = movie_containers[0].h3.find('span', class_='lister-item-year text-muted unbold').text.strip("() ")
# print(first_year)

first_imdb = float(movie_containers[0].strong.text)
# print(first_imdb)

first_metascore = int(movie_containers[0].find("span", class_="metascore favorable").text)
# print(first_metascore)

first_votes = movie_containers[37].find("span", attrs={"name": "nv"})
first_votes = int(first_votes["data-value"])
# print(first_votes)
# print('*' * 50)

# ------ Scraping one page ------

names = []
years = []
imbd_rating = []
metascores = []
votes = []

for container in movie_containers:
    if container.find('div', class_='ratings-metascore') is not None:
        name = container.h3.a.text
        names.append(name)

        year = container.find('span', class_='lister-item-year text-muted unbold').text.strip("(I) ")
        years.append(year)

        imbd = float(container.strong.text)
        imbd_rating.append(imbd)

        m_score = container.find('span', class_='metascore').text
        metascores.append(int(m_score))

        vote = container.find('span', attrs={'name': 'nv'})['data-value']
        votes.append(int(vote))
# print(years)
# print('*' * 50)

test_df = pd.DataFrame({
    'movies': names,
    'year': years,
    'imbd': imbd_rating,
    'metascore': metascores,
    'votes': votes
})

test_df['year'] = pd.to_datetime(test_df['year'])
print(type(test_df.info()))
