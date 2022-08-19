import pandas as pd
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

urls = "https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168"

content = requests.get(urls).content
soup = BeautifulSoup(content, 'html.parser')

"""
        Extract all information from an element
"""
forcast_items = soup.find(id="seven-day-forecast").find_all(class_="tombstone-container")
today = forcast_items[0]

# print(today.prettify())
# pretty to make result in HTML format

name = today.find(class_="period-name").get_text()
short_desc = today.find(class_="short-desc").get_text()
temp = today.find_all(class_="temp")[0].text

img = today.find("img")
# img is a dict, so we can get title with []
desc = img["title"]

"""
        Extract all information from a page
"""

seven_day = soup.find(id="seven-day-forecast-container")
period_tag = seven_day.select(".tombstone-container .period-name")
periods = [period.get_text() for period in period_tag]

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [tmp.get_text() for tmp in seven_day.select(".tombstone-container .temp")]
descs = [d['title'] for d in seven_day.select(".tombstone-container img")]

"""
        Show results on Pandas
"""

weather = pd.DataFrame({
    "period": periods,
    "short_desc": short_descs,
    "temp": temps,
    "desc": descs
})

print(tabulate(weather, headers='keys', tablefmt='psql'))
