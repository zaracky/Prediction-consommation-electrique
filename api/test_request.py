import requests

url = "http://localhost:3000/predict_single"

data = {
    "NumberofBuildings": 1,
    "LargestPropertyUseTypeGFA": 12000.0,
    "PropertyGFATotal": 18000.0,
    "SiteEUI_kBtu_sf": 58.0,
    "PropertyGFABuilding_s": 17000.0,
    "SourceEUIWN_kBtu_sf": 61.0,
    "SiteEUIWN_kBtu_sf": 59.0,
    "GHGEmissionsIntensity": 6.5,
    "NumberofFloors": 5,
    "ENERGYSTARScore": 85.0,
    "SourceEUI_kBtu_sf": 63.0,
    "PrimaryPropertyType": "Office",
    "Neighborhood": "Downtown"
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
