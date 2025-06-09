import re
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from core.embedding import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
You are an AI assistant tasked with providing accurate and clear answers using only the information given in the context below, except in the case of programming/code-related questions.

Context:
{context}

---

Instructions:
- Your answers must be based entirely on the context, **unless** the question is about programming or code and the context does not provide enough information.
- For programming-related questions, if the context lacks sufficient detail, you may use your general programming knowledge (e.g., syntax, common patterns).
- Clearly separate what is based on the context vs. what is general knowledge, if applicable.
- For all other types of questions, do not use any outside knowledge.
- You may provide code examples or technical explanations only if relevant to the question.
- Your response must be in the same language as the user's question.
- Be concise, clear, and informative.

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

    model = OllamaLLM(model="qwen3:1.7b")
    response = model.invoke(prompt)

    # Extrair conteúdo do <think>
    think_match = re.search(r"<think>(.*?)</think>", response, re.DOTALL)
    thinking = think_match.group(1).strip() if think_match else ""

    # Remover <think>...</think> da resposta para exibir só o final
    answer = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL).strip()

    return answer
