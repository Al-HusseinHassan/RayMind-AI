# RAG Pipeline

## Load PDF documents

Read all PDFs from the documents/ directory.

## Attach metadata

Add disease, section, filename, and page number to each document.

## Split documents into chunks

Divide long documents into smaller text sections.

## Generate embeddings

Convert each chunk into a numerical vector.

## Store embeddings in ChromaDB

Save vectors, text, and metadata in a persistent vector database.

## Build the retriever

Allow the application to search for relevant chunks based on a user's question.
