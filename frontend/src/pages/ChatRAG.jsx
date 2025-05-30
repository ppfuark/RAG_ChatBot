import React, { useState } from "react";
import axios from "axios";

const ChatRAG = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/rag/ask", {
        question: question,
      });

      console.log(response.data.answer);
      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer("Erro ao conectar com o servidor.");
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Chat RAG</h1>

      <textarea
        className="w-full p-2 border rounded mb-2"
        rows="3"
        placeholder="Digite sua pergunta..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      ></textarea>

      <button
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        onClick={handleSend}
        disabled={loading}
      >
        {loading ? "Enviando..." : "Enviar"}
      </button>

      {answer && (
        <div className="mt-4 p-3 bg-gray-100 border rounded whitespace-pre-line">
          <strong>Resposta:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default ChatRAG;
