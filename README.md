# Project Structure

This document explains the project's directory structure and the responsibility of each folder and file.

```text
project/
│
├── ml_model/
│   ├── model/
│   ├── preprocessing/
│   └── prediction.py
│
├── chatbot/
│   │
│   ├── knowledge/
│   │   ├── documents/
│   │   ├── document_loader.py
│   │   ├── text_splitter.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── llm/
│   │   ├── model.py
│   │   ├── prompts.py
│   │   └── conversation.py
│   │
│   └── rag_pipeline.py
│
└── app.py
```

## 1. `ml_model/`

Responsible for X-ray image classification and disease prediction.

| File / Folder    | Description                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `model/`         | Stores trained ML model files.                                                                                                 |
| `preprocessing/` | Contains image preprocessing functions required before model inference.                                                        |
| `prediction.py`  | Loads the trained model, receives an X-ray image, performs prediction, and returns the predicted disease and confidence score. |

## 2. `chatbot/`

Contains the components responsible for building the interactive medical chatbot.

### 2.1 `knowledge/`

Responsible for collecting, processing, storing, and retrieving medical information.

| File / Folder        | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| `documents/`         | Stores medical documents collected from trusted sources.             |
| `document_loader.py` | Loads medical documents from different file formats.                 |
| `text_splitter.py`   | Splits loaded documents into smaller chunks for efficient retrieval. |
| `embeddings.py`      | Converts document chunks into numerical vector representations.      |
| `vector_store.py`    | Stores and manages document embeddings in a vector database.         |
| `retriever.py`       | Retrieves relevant document chunks based on user queries.            |

### 2.2 `llm/`

Responsible for language model integration and conversational management.

| File              | Description                                                                  |
| ----------------- | ---------------------------------------------------------------------------- |
| `model.py`        | Initializes the LLM and provides an interface for interacting with it.       |
| `prompts.py`      | Defines system prompts and instructions that guide the LLM's behavior.       |
| `conversation.py` | Manages conversation history and maintains context across user interactions. |

### 2.3 `rag_pipeline.py`

Connects the Knowledge and LLM components.

- Receives user queries and the predicted disease as context.
- Calls the retriever to obtain relevant medical information.
- Passes retrieved information and conversation context to the LLM.
- Returns generated responses along with their references.

## 3. `app.py`

The main application entry point.

Responsible for:

- Providing the user interface.
- Handling X-ray image uploads.
- Displaying ML prediction results.
- Providing the interactive chatbot interface.
- Connecting the ML model and chatbot components.

---

**Note:** The project structure may evolve as new features and requirements are introduced.
