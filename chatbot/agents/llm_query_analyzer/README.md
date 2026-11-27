# Query Analyzer

## Overview

The Query Analyzer is the first LLM component in the chatbot's RAG pipeline.

Its primary responsibility is to understand the user's question, extract relevant metadata, and prepare the query for the retrieval process.

It acts as an intelligent preprocessing component between the user and the Retriever.

## Architecture

```text
             User Input
                  |
                  v
          +----------------+
          | Query Analyzer |
          |     Gemini     |
          +----------------+
                  |
          +-------+-------+
          |               |
          v               v
      Query Content   Metadata
          |               |
          +-------+-------+
                  |
                  v
              Retriever
```

## Model

**Provider:** Google

**Model:** Gemini 3.5 Flash-Lite

**Model ID:** `gemini-3.5-flash-lite`

The model is selected for its low latency, cost efficiency, multimodal capabilities, and structured output support.

Official documentation: https://ai.google.dev/gemini-api/docs/models

## Input

The Query Analyzer receives:

| Parameter              | Description                                  |
| ---------------------- | -------------------------------------------- |
| `user_query`           | Original question submitted by the user      |
| `prediction`           | ML model prediction, when available          |
| `confidence`           | ML prediction confidence, when available     |
| `conversation_history` | Previous conversation context, when relevant |

Example:

```python
{
    "user_query": "What are the common symptoms of pneumonia?",
    "prediction": "pneumonia",
    "confidence": 0.94
}
```

## Output

The Query Analyzer generates structured information containing:

| Field     | Description                               |
| --------- | ----------------------------------------- |
| `query`   | Query content used for semantic retrieval |
| `disease` | Relevant disease metadata                 |
| `section` | Relevant document section metadata        |

Example:

```json
{
    "query": "What are the common symptoms of pneumonia?",
    "disease": ["pneumonia"],
    "section": ["symptoms"]
}
```

### Supported Metadata

**Disease:**

- `healthy`
- `lung_cancer`
- `pneumonia`
- `covid`

**Section:**

- `overview`
- `symptoms`
- `risk_factors_and_complications`
- `diagnosis`
- `treatment`
- `normal_imaging`

The analyzer must only return metadata values that exist in the knowledge base.

## Responsibilities

1. Understand the user's question and identify its intent.
2. Identify relevant diseases and document sections.
3. Generate or refine the query for semantic retrieval.
4. Produce structured output for the Retriever.
5. Use conversation history to resolve references when necessary.
6. Avoid unnecessary metadata filtering when the question is broad or ambiguous.

## Important Considerations

- The original user question must be preserved for the Response Generator.
- ML predictions provide additional context but must not override the user's question.
- The analyzer must not invent disease or section metadata.
- Multiple diseases may be selected for comparison questions.
- If the relevant metadata cannot be determined confidently, retrieval should proceed without that filter.
- Image processing is not part of the initial Query Analyzer workflow. Its initial responsibility is text-based query analysis.

## Directory Structure

```text
query_analyzer/
├── README.md
├── model.py
├── prompt.py
└── analyzer.py
```

| File          | Responsibility                                   |
| ------------- | ------------------------------------------------ |
| `model.py`    | Initialize and configure the Gemini model.       |
| `prompt.py`   | Define the Query Analyzer instructions.          |
| `analyzer.py` | Analyze user input and return structured output. |
