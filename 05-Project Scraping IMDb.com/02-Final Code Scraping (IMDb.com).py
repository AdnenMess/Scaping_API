from random import randint
from time import sleep, time
from warnings import warn

import pandas as pd
from IPython.display import clear_output
from bs4 import BeautifulSoup
from requests import get
from tabulate import tabulate

"""
Modification liée au changement de structure de l'url de recherche
L'url n'est plus classée par page, mais par premier élément
Chaque page de recherche contient toujours 50 films
Donc voici le nouvel url de recherche avec first_film qui prendra les valeurs 1, 51, 101,...:
'https://www.imdb.com/search/title?release_date='+ year_url +'&sort=num_votes,desc&start='+ start
"""

starts = [str(i) for i in range(1, 201, 50)]

years_url = [str(i) for i in range(2002, 2022)]

# 1. Redéclarer les listes
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# 2. préparer l'affichage des boucles
start_time = time()
requests = 0

# 3. Pour chaque année de l'intervalle 2000-2017
for year_url in years_url:

    # 4. boucle sur starts contenant les premiers films des pages de 1 - 4
    for start in starts:

        # 5. Faire une requête GET
        response = get(
            'https://www.imdb.com/search/title?release_date=' + year_url + '&sort=num_votes,desc&start=' + start)

        # 6. Pause la boucle de 8 à 15 secondes
        sleep(randint(8, 15))

        # 7. Afficher les informations sur les requêtes
        requests += 1
        elapsed_time = time() - start_time
        print('Request: {}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
        clear_output(wait=True)

        # 8. Avertir si le code status est différent de 200
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # 9. Stopper la boucle si le nombre de requêtes est supérieur à 72
        if requests > 72:
            warn('Nombre de requêtes trop important')
            break

        # 10. Extraire le HTML avec BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # 11. Sélectionner les 50 films de chaque page (conteneur)
        mv_containers = page_html.find_all('div', class_="lister-item mode-advanced")

        # 12. Boucle pour chaque conteneur
        for container in mv_containers:
            # 13. Si le film a un Metascore
            if container.find('div', class_='ratings-metascore') is not None:
                # 14. scrape le titre
                name = container.h3.a.text
                names.append(name)

                # 15. scrape l'année
                year = container.h3.find('span', class_='lister-item-year').text.strip("(I) ")
                years.append(year)

                # 16. scrape la note IMDB
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # 17. scrape le Metascore
                metascore = container.find('span', class_='metascore').text
                metascores.append(int(metascore))

                # 18. scrape le nombre de votes
                vote = container.find('span', attrs={'name': 'nv'})['data-value']
                votes.append(int(vote))

# Afficher les 100 premiers films dans un DataFrame
movie_ratings = pd.DataFrame({
    'movie': names,
    'year': years,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes
})


movie_ratings.to_csv('imdb.csv', index=0)

print(tabulate(movie_ratings.head(100), headers='keys', tablefmt='psql'))
