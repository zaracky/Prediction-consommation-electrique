import requests

url = "http://localhost:3000/predict_list"

data = {
    "buildings": [
        {
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
        },
        {
            "NumberofBuildings": 2,
            "LargestPropertyUseTypeGFA": 15000.0,
            "PropertyGFATotal": 24000.0,
            "SiteEUI_kBtu_sf": 62.0,
            "PropertyGFABuilding_s": 23000.0,
            "SourceEUIWN_kBtu_sf": 67.0,
            "SiteEUIWN_kBtu_sf": 60.0,
            "GHGEmissionsIntensity": 8.1,
            "NumberofFloors": 6,
            "ENERGYSTARScore": 72.0,
            "SourceEUI_kBtu_sf": 69.0,
            "PrimaryPropertyType": "Hospital",
            "Neighborhood": "Capitol Hill"
        }
    ]
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
