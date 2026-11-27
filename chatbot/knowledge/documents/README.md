# Respiratory Disease Knowledge Base

## Overview

This directory contains the medical PDF documents used to build RayMind AI's local RAG knowledge base.

The documents provide introductory medical information related to the four classes supported by the machine learning classification models:

- `healthy/`
- `lung_cancer/`
- `pneumonia/`
- `covid/`

## Directory Structure

Each disease folder contains the following documents:

```text
documents/
│
├── healthy/
│   ├── overview.pdf
│   └── normal_imaging.pdf
│
├── lung_cancer/
│   ├── overview.pdf
│   ├── symptoms.pdf
│   ├── risk_factors_and_complications.pdf
│   ├── diagnosis.pdf
│   └── treatment.pdf
│
├── pneumonia/
│   ├── overview.pdf
│   ├── symptoms.pdf
│   ├── risk_factors_and_complications.pdf
│   ├── diagnosis.pdf
│   └── treatment.pdf
│
└── covid/
    ├── overview.pdf
    ├── symptoms.pdf
    ├── risk_factors_and_complications.pdf
    ├── diagnosis.pdf
    └── treatment.pdf
```

### Document Categories

| Document                             | Description                                                        |
| ------------------------------------ | ------------------------------------------------------------------ |
| `overview.pdf`                       | General introduction and background information about the disease. |
| `symptoms.pdf`                       | Common symptoms and clinical manifestations.                       |
| `risk_factors_and_complications.pdf` | Risk factors and potential complications.                          |
| `diagnosis.pdf`                      | Diagnostic methods and relevant medical examinations.              |
| `treatment.pdf`                      | General treatment approaches and management information.           |
| `normal_imaging.pdf`                 | Introductory information about normal medical imaging findings.    |

The `healthy/` folder contains only `overview.pdf` and `normal_imaging.pdf`, since the remaining disease-specific categories are not applicable in the same way.

## Important Class-Label Interpretation

`Healthy` is a machine learning class label, not a medical diagnosis or a guarantee that a person is disease-free.

The model's prediction and confidence score must always be presented as model-generated output rather than clinical certainty.

## RAG Ingestion and Metadata

Medical documents are processed through the knowledge ingestion pipeline:

1. Load PDF documents.
2. Split their content into smaller text chunks.
3. Generate embeddings using the configured Hugging Face embedding model.
4. Store the embeddings and associated metadata in ChromaDB.
5. Retrieve relevant chunks based on user queries and metadata filters.

Each document chunk should preserve metadata that identifies its origin and medical context.

Example metadata:

```python
{
    "disease": "pneumonia",
    "section": "diagnosis",
    "source": "diagnosis.pdf",
    "page": 2
}
```

This metadata enables the Retriever to apply relevant filters and improve retrieval accuracy.

## Retrieval Considerations

- Do not restrict retrieval automatically to the disease predicted by the ML model.
- The user's actual question determines which medical information is relevant.
- Model predictions may provide additional context but should not override the user's intent.
- General questions should be allowed to retrieve information across multiple disease categories.
- Metadata filters should only be applied when relevant information can be identified confidently.

For example, if the model predicts pneumonia but the user asks about lung cancer symptoms, the Retriever should retrieve relevant lung cancer information rather than restricting results to pneumonia.

## Medical Safety

The documents in this knowledge base are educational resources, not clinical guidelines or substitutes for professional medical advice.

Important considerations:

- Medical information should be reviewed against reliable and up-to-date clinical sources.
- The documents should be supplemented with current medical guidance before any real-world clinical use.
- Predictions from CT, CXR, or cough sound spectrogram images are not confirmed diagnoses.
- The chatbot must not prescribe medications or provide medication dosages.
- Users should be encouraged to consult qualified healthcare professionals for medical evaluation and treatment decisions.
