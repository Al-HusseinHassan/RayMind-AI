# Respiratory Disease Knowledge Base

This folder contains introductory PDFs for the four model classes:

- `healthy/`
- `lung_cancer/`
- `pneumonia/`
- `covid/`

Each disease folder contains:
- `overview.pdf`
- `symptoms.pdf`
- `risk_factors_and_complications.pdf`
- `diagnosis.pdf`
- `treatment.pdf`

The `healthy/` folder contains:
- `overview.pdf`
- `normal_imaging.pdf`

## Important class-label interpretation

`Healthy` is a model class label, not a medical diagnosis or a guarantee that a person is disease-free. The model's prediction and confidence must be presented as model output, not clinical certainty.

## RAG ingestion suggestions

Preserve source filename, page number (where available), class/disease label, and section as metadata. Example metadata:

```python
{
    "disease": "pneumonia",
    "section": "diagnosis",
    "source": "diagnosis.pdf",
    "page": 2
}
```

Do not force retrieval to use only the predicted class. A user may ask general questions or ask about a different disease. Treat the model prediction as context, and retrieve relevant material for the actual question.

## Medical safety

These documents are educational starting material, not clinical guidelines. Review the cited source pages and replace or supplement content with current local guidance before real-world use. AI outputs from CT, CXR, or cough audio are not confirmed diagnoses. The chatbot should encourage professional evaluation and must not prescribe medication or doses.
