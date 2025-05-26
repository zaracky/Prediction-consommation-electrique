# Prediction-consommation-electrique
Dans le cadre du plan de neutralité carbone de la ville de Seattle pour 2050, ce projet vise à prédire la consommation d'énergie des bâtiments non résidentiels à partir de leurs caractéristiques structurelles (surface, année de construction, type d'usage, etc.).
Les données proviennent du benchmark énergétique 2016 de Seattle

##  Objectif
-  Prédiction sur un bâtiment ou une liste (`/predict_single`, `/predict_list`)
-  Validation robuste des données en entrée avec **Pydantic**
-  Modèles pré-entraînés `RandomForestRegressor`
-  Déploiement cloud-ready avec BentoML & Docker

## Organisation du Projet
### Partie 1 – Modélisation Prédictive

#### 1. Analyse exploratoire des données 
- Mise en place de l’environnement de travail (Python, bibliothèques)

- Étude des types de bâtiments les plus représentatifs

- Repérage et traitement des valeurs aberrantes

- Définition de la cible à prédire (SiteEnergyUse / TotalGHGEmissions)

- Visualisations pour comprendre les relations entre variables

#### 2. Création de nouvelles variables
   
- Construction de nouvelles features à partir de :

- L’emplacement géographique

- L’année de construction

- Les types d’usages

- La taille et la structure du bâtiment

- Précautions contre le data leakage

#### 3. Préparation des données

- Nettoyage des valeurs extrêmes

- Encodage des variables catégorielles

- Analyse des corrélations

- Normalisation des variables numériques

#### 4. Modélisation
   
- Séparation des jeux d’entraînement et de test

- Validation croisée pour une meilleure robustesse

- Comparaison de plusieurs modèles de régression

- Optimisation des hyperparamètres (GridSearchCV)

- Analyse de l’importance des variables explicatives

### Partie 2 – Création et Déploiement de l’API

#### 1. Développement de l’API
- Sérialisation des modèles avec BentoML

- Implémentation de l’API via main_service.py

- Ajout de la validation des données avec Pydantic (type checking + règles métiers)

- Tests locaux via Swagger UI et scripts Python

#### 2. Déploiement cloud
- Rédaction d’un fichier bentofile.yaml pour le packaging

- Containerisation avec Docker via BentoML

- Déploiement de l’image sur Google Cloud Run

- Tests de l’API accessible en ligne (requêtes unitaires + lots)



## Structure du projet
Le projet contient les fichiers suivants :

    Prediction-consommation-electrique/
    ├── api/
     └── service.py # Script principal de l’API
     └── bentofile.yaml # Config BentoML
     └── test_request.py # Script de test local
     ├── saved_models/# Modèles sauvegardés
    │── data/           # donnée utilisét
    ├── notebook/             # notebook utilisé pour analyse exploratoire/feature engineering


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
