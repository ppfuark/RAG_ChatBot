import re
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from core.embedding import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an AI assistant tasked with providing accurate and clear answers using only the information given in the context below.

Context:
{context}

---

Instructions:
- Carefully analyze the context above.
- Your answer must be entirely based on this content. Do not use outside knowledge.
- If the context refers to a specific section of a document (e.g., "Section 6") that is not fully visible, you should provide a brief and general summary based on what is mentioned about that section in the visible context.
- If the requested information is not clearly available, state that explicitly.
- Your response must be in the same language as the user's question.
- Be concise, clear, and informative in your explanation.

Question:
{question}

Answer:
"""


def query_rag(question: str):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(question, k=5)
    context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context,
        question=question
    )

    model = OllamaLLM(model="llama3.2:latest")
    response = model.invoke(prompt)

    # Extrair conteúdo do <think>
    think_match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
    thinking = think_match.group(1).strip() if think_match else ""

    # Remover <think>...</think> da resposta para exibir só o final
    answer = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    return answer
