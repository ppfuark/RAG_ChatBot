import React from "react";

export default function Input({ question, setQuestion, loading, error, handleSend, handleKeyDown }) {
  return (
    <div className="border-t p-4 bg-gray-50">
      {error && (
        <div className="mb-3 p-2 bg-red-50 text-red-600 text-sm">{error}</div>
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
          className="bg-[#9f2ad1] text-white px-6 py-2 rounded-lg hover:bg-[#8a1bc2] focus:outline-none focus:ring-2 focus:ring-[#9f2ad1] focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          onClick={handleSend}
          disabled={loading || !question.trim()}
        >
          {loading ? (
            <span className="inline-flex items-center">
              <svg
                className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
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
  );
}
