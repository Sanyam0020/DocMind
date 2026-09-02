import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [file, setFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)

  async function uploadDocument() {
    if (!file) {
      setUploadStatus('Please select a PDF first.')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    setLoading(true)
    setUploadStatus('Uploading document...')

    try {
      const response = await fetch(
        `${API_URL}/documents/upload`,
        {
          method: 'POST',
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Upload failed.')
      }

      setUploadStatus(
        `Uploaded ${data.filename} — ${data.chunks} chunks created.`
      )
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  async function askQuestion() {
    if (!question.trim()) {
      return
    }

    setLoading(true)
    setAnswer('')
    setResults([])

    try {
      const response = await fetch(
        `${API_URL}/ask`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            question: question,
          }),
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Question failed.')
      }

      setAnswer(data.answer)
      setResults(data.results || [])
    } catch (error) {
      setAnswer(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>DocuMind</h1>
        <p>Ask questions about your documents using RAG + AI.</p>
      </header>

      <main className="container">
        <section className="card">
          <h2>Upload Document</h2>

          <input
            type="file"
            accept=".pdf,.txt"
            onChange={(event) => setFile(event.target.files[0])}
          />

          <button
            type="button"
            onClick={uploadDocument}
            disabled={loading}
          >
            Upload
          </button>

          {file && (
            <p className="file-name">
              Selected: {file.name}
            </p>
          )}

          {uploadStatus && (
            <p className="status">
              {uploadStatus}
            </p>
          )}
        </section>

        <section className="card">
          <h2>Ask DocuMind</h2>

          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question about your document..."
            rows="4"
          />

          <button
            type="button"
            onClick={askQuestion}
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Ask Question'}
          </button>
        </section>

        {answer && (
          <section className="card">
            <h2>Answer</h2>

            <div className="answer">
              {answer}
            </div>
          </section>
        )}

        {results.length > 0 && (
          <section className="card">
            <h2>Retrieved Sources</h2>

            {results.map((result) => (
              <div
                className="source"
                key={`${result.chunk_id}-${result.page_number}`}
              >
                <div>
                  <strong>
                    Chunk {result.chunk_id}
                  </strong>
                  {' — '}
                  Page {result.page_number}
                </div>

                <div className="score">
                  Score: {result.score.toFixed(3)}
                </div>

                <p>{result.text}</p>
              </div>
            ))}
          </section>
        )}
      </main>
    </div>
  )
}

export default App