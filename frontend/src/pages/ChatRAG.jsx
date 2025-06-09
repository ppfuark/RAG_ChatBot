import React, { useState } from "react";
import Header from "../components/Header";
import Input from "../components/Input";
import Sidebar from "../components/Sidebar";

const ChatRAG = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [conversation, setConversation] = useState([]);

  const handleSend = async () => {
    if (!question.trim()) {
      setError("Please enter a question");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      setConversation((prev) => [
        ...prev,
        {
          sender: "user",
          message: question,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);

      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 300000); // 300s

      const response = await fetch("/rag/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
        signal: controller.signal,
      });

      clearTimeout(timeout);

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      const botAnswer = data.answer;

      setAnswer(botAnswer);
      setConversation((prev) => [
        ...prev,
        {
          sender: "bot",
          message: botAnswer,
          timestamp: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          }),
        },
      ]);
    } catch (error) {
      let errorMessage = "Error connecting to the server";
      if (error.name === "AbortError") {
        errorMessage = "Request timeout";
      } else if (error.message.includes("Server error")) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      console.error("API Error:", error);
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-screen bg-gray-50 flex">
      <div>
        <Sidebar />
      </div>
      <div className="w-6xl mx-auto bg-white shadow-md overflow-hidden">
        <Header />
        <div className="h-150 p-4 overflow-y-auto space-y-4">
          {conversation.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-500">Start a conversation by asking a question</p>
            </div>
          ) : (
            conversation.map((item, index) => (
              <div
                key={index}
                className={`flex ${item.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg -lg px-4 py-2 ${
                    item.sender === "user"
                      ? "bg-[#f0d9ff] text-[#9f2ad1]"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  <p className="whitespace-pre-line">{item.message}</p>
                  <p
                    className={`text-xs mt-1 ${
                      item.sender === "user" ? "text-[#9f2ad1]" : "text-gray-500"
                    }`}
                  >
                    {item.timestamp}
                  </p>
                </div>
              </div>
            ))
          )}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 -lg px-4 py-2">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 -full bg-[#9f2ad1] animate-bounce"></div>
                  <div
                    className="w-2 h-2 -full bg-[#9f2ad1] animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                  <div
                    className="w-2 h-2 -full bg-[#9f2ad1] animate-bounce"
                    style={{ animationDelay: "0.4s" }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>

        <Input
          question={question}
          setQuestion={setQuestion}
          loading={loading}
          error={error}
          handleSend={handleSend}
          handleKeyDown={handleKeyDown}
        />
      </div>
    </div>
  );
};

export default ChatRAG;
