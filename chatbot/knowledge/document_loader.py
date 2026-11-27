import os
from langchain_community.document_loaders import PyPDFLoader
KNOWLEDGE_PATH = os.path.dirname(os.path.abspath(__file__))
DOCUMENTS_PATH = os.path.join(KNOWLEDGE_PATH, "documents")
diseases = os.listdir(DOCUMENTS_PATH)
documents_page_level = []
for disease in diseases:
    disease_path = os.path.join(DOCUMENTS_PATH, disease)
    if not os.path.isdir(disease_path):
        continue

    documents = os.listdir(disease_path)
    for document in documents:
        if not document.lower().endswith(".pdf"):
            continue
        document_path = os.path.join(disease_path, document)
        loader = PyPDFLoader(document_path)
        pages = loader.load()
        for page in pages:
            page.metadata.update({
                "disease":disease,
                "source":document_path,
                "section":os.path.splitext(document)[0]
            })
        documents_page_level.extend(pages)