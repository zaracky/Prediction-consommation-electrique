# Prediction-consommation-electrique
Dans le cadre du plan de neutralité carbone de la ville de Seattle pour 2050, ce projet vise à prédire la consommation d'énergie des bâtiments non résidentiels à partir de leurs caractéristiques structurelles (surface, année de construction, type d'usage, etc.).
Les données proviennent du benchmark énergétique 2016 de Seattle

##  Objectif
-  Prédiction sur un bâtiment ou une liste (`/predict_single`, `/predict_list`)
-  Validation robuste des données en entrée avec **Pydantic**
-  Modèles pré-entraînés `RandomForestRegressor`
-  Déploiement cloud-ready avec BentoML & Docker

##  Exemple d’entrée (`/predict_single`)


``{
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
}``

## Lancer en local
`bentoml serve main_service:svc`

Puis accéder à :
http://localhost:3000/


## Déploiement via Docker
`bentoml build`

`bentoml containerize energy_consumation_predictor:latest`

`docker run --rm -p 3000:3000 energy_consumation_predictor:latest`

## Déploiement sur GCP

`docker tag energy_consumation_predictor:latest gcr.io/<project-id>/energy-api`

`docker push gcr.io/<project-id>/energy-api`

`gcloud run deploy energy-api \
  --image gcr.io/<project-id>/energy-api \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated`
  
## Dépendances principales
- bentoml

- pydantic

- cloudpickle

- pandas

- scikit-learn
