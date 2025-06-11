import React, { useEffect, useState } from "react";

export default function Sidebar() {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const API = "http://127.0.0.1:8000/file";

  const fetchFiles = async () => {
    try {
      const res = await fetch(`${API}/`);
      const data = await res.json();
      setFiles(data);
    } catch (err) {
      console.error("Erro ao buscar arquivos:", err);
    }
  };

  const handleFileSelect = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Selecione um arquivo antes de enviar.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      await fetch(`${API}/`, {
        method: "POST",
        body: formData,
      });
      setSelectedFile(null);
      fetchFiles();
    } catch (err) {
      console.error("Erro ao enviar arquivo:", err);
    }
  };

  const handleView = (filename) => {
    window.open(`${API}/${filename}`, "_blank");
  };

  const handleDelete = async (filename) => {
    const confirmed = confirm(`Tem certeza que deseja deletar o arquivo "${filename}"?`);
    if (!confirmed) return;

    try {
      await fetch(`${API}/${filename}`, {
        method: "DELETE",
      });
      fetchFiles();
    } catch (err) {
      console.error("Erro ao deletar arquivo:", err);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <div className="w-full bg-[#9f2ad1] text-white p-6 h-screen overflow-auto shadow-md">
      <h2 className="text-xl font-semibold mb-6">Gerenciar Arquivos</h2>

      <label className="block mb-3">
        <span className="text-sm font-light mb-1 block">Selecionar arquivo para enviar</span>
        <input
          type="file"
          onChange={handleFileSelect}
          accept=".pdf"
          className="text-white bg-[#bf69e2] file:mr-4 file:py-2 file:px-4
                     file:rounded-md file:border-0 file:text-sm file:font-semibold
                     file:bg-white file:text-[#9f2ad1] hover:file:bg-gray-100"
        />
      </label>

      <button
        onClick={handleUpload}
        className="mb-6 bg-white text-[#9f2ad1] px-4 py-2 rounded hover:bg-gray-100"
      >
        Enviar arquivo
      </button>

      <ul className="space-y-4">
        {files.map((file, index) => (
          <li key={index} className="bg-white/10 rounded-lg p-3">
            <p className="font-medium text-white truncate">{file}</p>

            <div className="flex gap-3 mt-2 text-sm">
              <button
                onClick={() => handleView(file)}
                className="bg-white text-[#9f2ad1] px-2 py-1 rounded hover:bg-gray-100"
              >
                Ver
              </button>
              <button
                onClick={() => handleDelete(file)}
                className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
              >
                Deletar
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
