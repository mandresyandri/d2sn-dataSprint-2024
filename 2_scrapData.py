import requests
from bs4 import BeautifulSoup

url = "https://fr.wikipedia.org/wiki/Liste_des_gares_desservies_par_TGV"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

table_gares = soup.select_one("table:first-of-type")

# Vérifier si l'élément existe
if table_gares:
    print(table_gares)
else:
    print("Tableau non trouvé")