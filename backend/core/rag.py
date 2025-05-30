import re
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from core.embedding import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def query_rag(question: str):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(question, k=5)
    context = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE).format(
        context=context,
        question=question
    )

    model = OllamaLLM(model="mistral")
    response = model.invoke(prompt)

    # Extrair conteúdo do <think>
    think_match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
    thinking = think_match.group(1).strip() if think_match else ""

    # Remover <think>...</think> da resposta para exibir só o final
    answer = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    return answer
