import React, { useState } from "react";
import axios from "axios";

const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [summary, setSummary] = useState("");
  const [quiz, setQuiz] = useState("");
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [documentContent, setDocumentContent] = useState(""); // extracted text


  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleAsk = async () => {
  if (!question || !documentContent) return;

  try {
    const res = await axios.post("http://localhost:8000/ask", {
      content: documentContent,
      question: question,
    });

    setAnswer(res.data.answer);
  } catch (err) {
    console.error(err);
    alert("Failed to get an answer");
  }
};


  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setSummary(res.data.summary);
      setQuiz(res.data.quiz);
      setDocumentContent(res.data.summary); // or pass full text if returned

    } catch (error) {
      console.error("Upload error", error);
      alert("Upload failed. Check backend or file type.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>📄 AI Document Chatbot</h2>
      <input type="file" onChange={handleChange} accept=".pdf,.png,.jpg,.jpeg" />
      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? "Uploading..." : "Upload"}
      </button>

      {summary && (
        <div style={{ marginTop: 20 }}>
          <h3>🧠 Summary</h3>
          <pre>{summary}</pre>
        </div>
      )}

      {quiz && (
        <div style={{ marginTop: 20 }}>
          <h3>📋 Quiz</h3>
          <pre>{quiz}</pre>
        </div>
      )}
      <div style={{ marginTop: 40 }}>
  <h3>🧠 Ask a Question About the Document</h3>
  <input
    type="text"
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
    placeholder="Ask a question..."
    style={{ width: "80%", padding: "8px", marginRight: "10px" }}
  />
  <button onClick={handleAsk}>Ask</button>

  {answer && (
    <div style={{ marginTop: 20 }}>
      <strong>Answer t:</strong>
      <p>{answer}</p>
    </div>
  )}
</div>

    </div>
    
  );
};

export default FileUpload;
