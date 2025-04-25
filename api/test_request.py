import requests

# URL de ton API locale
url = "http://localhost:3000/predict"

# Données de test
payload = {
    "PropertyGFATotal": 15000,
    "YearBuilt": 1995,
    "NumberofFloors": 3,
    "PrimaryPropertyType": "Office",
    "Neighborhood": "Downtown"
}

# Envoi de la requête POST
response = requests.post(url, json=payload)

# Affichage de la réponse
print("Status Code:", response.status_code)
print("Réponse JSON:", response.json())
