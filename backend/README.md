# ⚙️ Backend - PDF Chatbot com LangChain

Este é o backend da aplicação de Chatbot que permite analisar o conteúdo de arquivos PDF e responder perguntas com base neles. Utiliza **LangChain**, **ChromaDB**, e **FastAPI** para lidar com processamento, armazenamento vetorial e resposta contextual.

---

## 🧠 Tecnologias

- Python 3.11+
- FastAPI
- LangChain
- ChromaDB
- PyPDF
- Boto3 (opcional, para armazenamento AWS)
- Pytest (para testes)

---

## 📦 Como instalar e rodar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Rodar a aplicação

```bash
uvicorn main:app --reload
```

> A API estará disponível em `http://127.0.0.1:8000`

---

## 📂 Estrutura do Projeto

```
backend/
├── api/
│   ├── routes/
│   │   ├── query.py
│   │   ├── upload.py
│   │   └── api.py
│   └── chroma/
├── core/
│   ├── embedding.py
│   ├── indexer.py
│   └── rag.py
├── data/
├── .gitignore
├── README.md
└── requirements.txt
```

---


