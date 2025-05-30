import React, { useState } from "react";
import axios from "axios";

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
      // Add user question to conversation with timestamp
      setConversation(prev => [...prev, { 
        sender: "user", 
        message: question,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
      
      const response = await axios.post("http://127.0.0.1:8000/rag/ask/", {
        question: question,
      }, {
        timeout: 300000 // 300 seconds timeout
      });

      const botAnswer = response.data.answer;
      setAnswer(botAnswer);
      // Add bot answer to conversation with timestamp
      setConversation(prev => [...prev, { 
        sender: "bot", 
        message: botAnswer,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } catch (error) {
      let errorMessage = "Error connecting to the server";
      if (error.response) {
        errorMessage = `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = "No response from server";
      } else if (error.code === 'ECONNABORTED') {
        errorMessage = "Request timeout";
      }
      
      setError(errorMessage);
      console.error("API Error:", error);
    } finally {
      setLoading(false);
      setQuestion(""); // Clear input after sending
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
        {/* Header */}
        <div className="bg-[#9f2ad1] p-6 text-white">
          <h1 className="text-2xl font-bold">Chat with RAG</h1>
          <p className="text-[#d9b3e8]">Ask questions and get answers from our knowledge base</p>
        </div>
        
        {/* Conversation history */}
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
                  className={`max-w-xs md:max-w-md lg:max-w-lg rounded-lg px-4 py-2 ${item.sender === "user" 
                    ? "bg-[#f0d9ff] text-[#9f2ad1]" 
                    : "bg-gray-100 text-gray-800"}`}
                >
                  <p className="whitespace-pre-line">{item.message}</p>
                  <p className={`text-xs mt-1 ${item.sender === "user" ? "text-[#9f2ad1]" : "text-gray-500"}`}>
                    {item.timestamp}
                  </p>
                </div>
              </div>
            ))
          )}
          
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 rounded-full bg-[#9f2ad1] animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-[#9f2ad1] animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  <div className="w-2 h-2 rounded-full bg-[#9f2ad1] animate-bounce" style={{animationDelay: '0.4s'}}></div>
                </div>
              </div>
            </div>
          )}
        </div>
        
        {/* Input area */}
        <div className="border-t p-4 bg-gray-50">
          {error && (
            <div className="mb-3 p-2 bg-red-50 text-red-600 rounded text-sm">
              {error}
            </div>
          )}
          
          <div className="flex space-x-2">
            <textarea
              className="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-[#9f2ad1] focus:border-[#9f2ad1]"
              rows="2"
              placeholder="Type your question here..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
            />
            
            <button
              className="bg-[#9f2ad1] text-white px-6 py-2 rounded-lg hover:bg-[#8a1bc2] 
                         focus:outline-none focus:ring-2 focus:ring-[#9f2ad1] focus:ring-offset-2
                         disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              onClick={handleSend}
              disabled={loading || !question.trim()}
            >
              {loading ? (
                <span className="inline-flex items-center">
                  <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Sending...
                </span>
              ) : (
                "Send"
              )}
            </button>
          </div>
          
          <p className="mt-2 text-xs text-gray-500">
            Press Shift+Enter for a new line, or just Enter to send
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatRAG;