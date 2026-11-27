from typing import Literal
from pydantic import BaseModel, Field


Section = Literal[
    "overview", "symptoms", "risk_factors_and_complications",
    "diagnosis", "treatment", "normal_imaging",
]
Disease = Literal["healthy", "lung_cancer", "pneumonia", "covid"]

Modality = Literal["CXR", "CT", "Cough Sound"]


class QueryRoute(BaseModel):
    """Classify a user question to select retrieval filters."""

    sections: list[Section] = Field(
        default_factory=list,
        description=(
            "All sections relevant to the question. "
            "Use 'normal_imaging' for how normal scans look. "
            "Empty if none apply."
        ),
    )
    diseases: list[Disease] = Field(
        default_factory=list,
        description=(
            "All conditions the question is about. "
            "Use 'healthy' only for questions about normal, disease-free lungs. "
            "Empty if the condition is unspecified or not in the allowed values."
        ),
    )

    modality: Modality | None = Field(
        default=None,
        description=(
            "The medical input type the question refers to: "
            "'CXR' for chest X-rays, 'CT' for CT scans, "
            "'Cough Sound' for spectrogram images. "
            "Use None if no type is mentioned, or if it is not one of these."
        ),
    )