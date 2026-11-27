# Query Analyzer

## Overview

The Query Analyzer is the first LLM component in RayMind AI's chatbot workflow.

Its primary responsibility is to understand the user's question, extract relevant metadata, and prepare the information required by the retrieval process.

It acts as an intelligent preprocessing component between the user and the Trigger, helping the system determine which medical knowledge is relevant to the request.

When an image is provided, the analyzer can also identify its imaging modality to guide the subsequent workflow.

## Architecture

```text
                User Input
             (Query + Optional Image)
                      |
                      v
             +------------------+
             |  Query Analyzer  |
             |       LLM        |
             +------------------+
                      |
             +--------+--------+
             |                 |
             v                 v
        Query Content       Metadata
                            - Diseases
                            - Sections
                            - Modality
             |                 |
             +--------+--------+
                      |
                      v
                   Trigger
```

## Model

**Provider:** Google

**Model:** Google Gemini

The model is used to understand natural-language questions and generate structured metadata for the chatbot workflow.

Its capabilities support query understanding and structured information extraction.

Official documentation: https://ai.google.dev/gemini-api/docs/models

## Input

The Query Analyzer receives:

| Parameter    | Description                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------ |
| `user_query` | Original question submitted by the user.                                                         |
| `image_path` | Optional path to an uploaded medical image, used when image modality identification is required. |

Example:

```python
query = "What are the common symptoms of pneumonia?"
image_path = None
```

For image-related requests, an image path can also be provided.

## Output

The Query Analyzer generates structured metadata containing:

| Field      | Description                                   |
| ---------- | --------------------------------------------- |
| `sections` | Relevant medical knowledge-base sections.     |
| `diseases` | Relevant disease categories.                  |
| `modality` | Identified imaging modality, when applicable. |

Example:

```python
{
    "sections": ["symptoms"],
    "diseases": ["pneumonia"],
    "modality": None
}
```

For an image-related request, the modality may be identified as `CT`, `CXR`, or another supported value.

### Supported Metadata

**Diseases:**

- `healthy`
- `lung_cancer`
- `pneumonia`
- `covid`

**Sections:**

- `overview`
- `symptoms`
- `risk_factors_and_complications`
- `diagnosis`
- `treatment`
- `normal_imaging`

**Imaging Modalities:**

- `CT`
- `CXR`

The analyzer must use valid metadata values supported by the knowledge base and prediction workflow.

## Responsibilities

1. Understand the user's question and identify its intent.
2. Identify relevant diseases and document sections.
3. Identify the imaging modality when an image is provided.
4. Generate structured metadata for the subsequent workflow.
5. Support questions involving multiple diseases or medical topics.
6. Avoid unnecessary metadata filtering when the question is broad or ambiguous.

## Important Considerations

- The original user question must be preserved for the Response Generator.
- ML predictions must not override the user's actual question.
- The analyzer must not invent disease or section metadata.
- Multiple diseases may be selected for comparison questions.
- If relevant metadata cannot be determined confidently, the corresponding filter should be omitted.
- Modality identification helps guide the workflow but does not replace validation of the actual uploaded image.
- The Query Analyzer does not execute ML predictions or retrieve documents; these operations are handled by the Trigger.

## Directory Structure

```text
llm_query_analyzer/
├── model.py
├── prompt.py
├── schema.py
└── agent.py
```

| File        | Responsibility                                                                 |
| ----------- | ------------------------------------------------------------------------------ |
| `model.py`  | Initializes and configures the Gemini model.                                   |
| `prompt.py` | Defines the instructions that guide query analysis.                            |
| `schema.py` | Defines the structured output schema used to validate the analyzer's response. |
| `agent.py`  | Builds and executes the Query Analyzer agent and returns structured metadata.  |
