from __future__ import annotations
import bentoml
import pandas as pd
import cloudpickle
from pydantic import BaseModel, field_validator
from typing import List
from bentoml.io import JSON

# 📦 Chargement des pipelines
def load_pipeline(filename):
    with open(filename, 'rb') as f:
        return cloudpickle.load(f)

# 📄 Modèles Pydantic
class Building(BaseModel):
    NumberofBuildings: int
    LargestPropertyUseTypeGFA: float
    PropertyGFATotal: float
    SiteEUI_kBtu_sf: float
    PropertyGFABuilding_s: float
    SourceEUIWN_kBtu_sf: float
    SiteEUIWN_kBtu_sf: float
    GHGEmissionsIntensity: float
    NumberofFloors: int
    ENERGYSTARScore: float
    SourceEUI_kBtu_sf: float
    PrimaryPropertyType: str
    Neighborhood: str

    @field_validator(
        'PropertyGFATotal',
        'SiteEUI_kBtu_sf',
        'GHGEmissionsIntensity',
        'SourceEUI_kBtu_sf'
    )
    @classmethod
    def validate_positive(cls, value, field):
        if value < 0:
            raise ValueError(f"{field.name} doit être positif")
        return value

    def rename_to_dataset_columns(self) -> dict:
        return {
            "NumberofBuildings": self.NumberofBuildings,
            "LargestPropertyUseTypeGFA": self.LargestPropertyUseTypeGFA,
            "PropertyGFATotal": self.PropertyGFATotal,
            "SiteEUI(kBtu/sf)": self.SiteEUI_kBtu_sf,
            "PropertyGFABuilding(s)": self.PropertyGFABuilding_s,
            "SourceEUIWN(kBtu/sf)": self.SourceEUIWN_kBtu_sf,
            "SiteEUIWN(kBtu/sf)": self.SiteEUIWN_kBtu_sf,
            "GHGEmissionsIntensity": self.GHGEmissionsIntensity,
            "NumberofFloors": self.NumberofFloors,
            "ENERGYSTARScore": self.ENERGYSTARScore,
            "SourceEUI(kBtu/sf)": self.SourceEUI_kBtu_sf,
            "PrimaryPropertyType": self.PrimaryPropertyType,
            "Neighborhood": self.Neighborhood
        }

class BuildingList(BaseModel):
    buildings: List[Building]

    def rename_all(self) -> List[dict]:
        return [b.rename_to_dataset_columns() for b in self.buildings]

# 🚀 Création du service BentoML
svc = bentoml.Service(name="energy_consumation_predictor")

# 🔧 Chargement des modèles
pipeline = load_pipeline("random_forest_energy_model.pipeline")
pipeline_ghg = load_pipeline("random_forest_co2_model.pipeline")

# 🔮 Prédiction sur un bâtiment
@svc.api(input=JSON(pydantic_model=Building), output=JSON())
def predict_single(input_data: Building) -> dict:
    try:
        df = pd.DataFrame([input_data.rename_to_dataset_columns()])
        X = pipeline.named_steps['preprocessing'].transform(df)
        X_ghg = pipeline_ghg.named_steps['preprocessing'].transform(df)

        y_energy = pipeline.named_steps['regressor'].predict(X)[0]
        y_ghg = pipeline_ghg.named_steps['regressor'].predict(X_ghg)[0]

        return {
            "prediction": {
                "SiteEnergyUse(kBtu)": round(float(y_energy), 2),
                "TotalGHGEmissions": round(float(y_ghg), 2)
            },
            "status_code": 200
        }
    except Exception as e:
        return {"error": str(e), "status_code": 500}

# 🔮 Prédiction sur une liste de bâtiments
@svc.api(input=JSON(pydantic_model=BuildingList), output=JSON())
def predict_list(input_data: BuildingList) -> dict:
    try:
        df = pd.DataFrame(input_data.rename_all())
        X = pipeline.named_steps['preprocessing'].transform(df)
        X_ghg = pipeline_ghg.named_steps['preprocessing'].transform(df)

        y_energy = pipeline.named_steps['regressor'].predict(X)
        y_ghg = pipeline_ghg.named_steps['regressor'].predict(X_ghg)

        predictions = [
            {
                "SiteEnergyUse(kBtu)": round(float(e), 2),
                "TotalGHGEmissions": round(float(g), 2)
            }
            for e, g in zip(y_energy, y_ghg)
        ]

        return {
            "predictions": predictions,
            "number_of_predictions": len(predictions),
            "status_code": 200
        }
    except Exception as e:
        return {"error": str(e), "status_code": 500}
