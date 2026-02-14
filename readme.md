# auto-rag-vs-basic

Testing RAG approches in Gen AI: Auto-RAG versus basic RAG with domain-specific configs.

For Auto-RAG, a first implementation attempt is done using RAG-Anything - https://github.com/HKUDS/RAG-Anything

Work in progress.

## Run

The initial implementation for Auto-RAG is in a Jupyter Notebook found in \auto-rag\notebook.ipynb

It's able to ingest a PDF, either simple or complex, and run queries on it.

## Initial setup

~ new virtual environment  
py -3.10 -m venv .venv

~ activate env  
.venv\Scripts\activate.bat

~ install all dependencies  
poetry install

## Documents to run RAG on

Any PDF documents can be used.

I've tested with public documents from the European Patent Office, the archive EPRTBJV2014000022001001.tar - it seems though that it's not legal to include them in this repo.

## Helpful commands

~ add new package  
poetry add package-name
