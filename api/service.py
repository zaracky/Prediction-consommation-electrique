import bentoml
import pandas as pd
from joblib import load
from pydantic import BaseModel, Field
from bentoml.io import JSON
from bentoml import Service

# Chargement du modèle
model = load("rf_pipeline_light.joblib")

# Définition du service
svc = Service("energy_prediction_service")

# Définition du schéma d'entrée
class BuildingInput(BaseModel):
    PropertyGFATotal: float = Field(..., gt=0)
    YearBuilt: int = Field(..., ge=1800, le=2025)
    NumberofFloors: float = Field(..., gt=0)
    PrimaryPropertyType: str
    Neighborhood: str

# Définition de l'API
@svc.api(input=JSON(pydantic_model=BuildingInput), output=JSON())
async def predict(input_data: BuildingInput) -> dict:
    input_df = pd.DataFrame([input_data.dict()])
    prediction = model.predict(input_df)
    return {"prediction_kBtu": round(prediction[0], 2)}
