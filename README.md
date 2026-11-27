# Project Structure

This document explains the project's directory structure and the responsibility of each folder and file.

```text
RayMind-AI/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
│
├── machine_learning_model/
│   ├── best_model_CT.keras
│   ├── best_model_CXR.keras
│   ├── best_model_Cough_sound.keras
│   ├── class_names.json
│   ├── config.json
│   └── prediction.py
│
└── chatbot/
    │
    ├── agents/
    │   ├── llm_query_analyzer/
    │   ├── trigger/
    │   └── llm_response_generator/
    │
    └── knowledge/
        ├── chroma_db/
        ├── documents/
        ├── document_loader.py
        ├── embeddings.py
        ├── text_splitter.py
        ├── vector_store.py
        └── retriever.py
```

## 1. `machine_learning_model/`

Responsible for classifying medical images and predicting respiratory diseases.

| File / Folder                  | Description                                                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `best_model_CT.keras`          | Trained deep learning model for CT scan classification.                                                                              |
| `best_model_CXR.keras`         | Trained deep learning model for chest X-ray classification.                                                                          |
| `best_model_Cough_sound.keras` | Trained deep learning model for cough sound spectrogram classification.                                                              |
| `class_names.json`             | Stores the class labels used by the prediction models.                                                                               |
| `config.json`                  | Contains model configuration settings.                                                                                               |
| `prediction.py`                | Loads the appropriate model, preprocesses the input image, performs inference, and returns the predicted class and confidence score. |

## 2. `chatbot/`

Contains the components responsible for the AI-powered medical chatbot, which combines language models with Retrieval-Augmented Generation (RAG).

### 2.1 `agents/`

Contains the agents and components responsible for processing user queries and generating responses.

| File / Folder             | Description                                                                                                                  |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `llm_query_analyzer/`     | Analyzes user queries using an LLM and extracts metadata, such as relevant diseases, medical topics, and imaging modalities. |
| `trigger/`                | Coordinates the chatbot workflow by determining when to retrieve medical information or execute image prediction.            |
| `llm_response_generator/` | Generates contextual responses using the LLM, retrieved medical knowledge, prediction results, and conversation history.     |

### 2.2 `knowledge/`

Responsible for collecting, processing, storing, and retrieving medical information.

| File / Folder        | Description                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| `documents/`         | Stores medical documents collected from trusted sources.                                 |
| `chroma_db/`         | Stores the medical knowledge embeddings in a persistent ChromaDB vector database.        |
| `document_loader.py` | Loads medical documents from PDF files.                                                  |
| `text_splitter.py`   | Splits loaded documents into smaller chunks for efficient retrieval.                     |
| `embeddings.py`      | Converts document chunks into numerical vector representations.                          |
| `vector_store.py`    | Creates and manages the ChromaDB vector store.                                           |
| `retriever.py`       | Retrieves relevant medical document chunks based on user queries and extracted metadata. |

## 3. `config.py`

Contains project-level configuration and path management, helping different modules access project resources consistently.

## 4. `app.py`

The main application entry point, built using Streamlit.

Responsible for:

- Providing the user interface.
- Handling medical image uploads.
- Displaying image classification results.
- Providing the interactive chatbot interface.
- Managing user conversations.
- Connecting the machine learning and chatbot components.

## 5. `requirements.txt`

Contains the Python dependencies required to install and run the project.

---

**Note:** The project is designed with modular components, allowing the machine learning models, knowledge retrieval system, and chatbot agents to be maintained and extended independently.
