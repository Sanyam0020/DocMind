import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [file, setFile] = useState(null)
  const [uploadMessage, setUploadMessage] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [results, setResults] = useState([])
  const [loadingUpload, setLoadingUpload] = useState(false)
  const [loadingQuestion, setLoadingQuestion] = useState(false)
  const [error, setError] = useState('')

  async function handleUpload() {
    if (!file) {
      setError('Please select a document first.')
      return
    }

    setError('')
    setUploadMessage('')
    setLoadingUpload(true)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${API_URL}/documents/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed with status ${response.status}`)
      }

      const data = await response.json()

      setUploadMessage(
        `Uploaded ${data.filename} — ${data.chunks} chunks created.`
      )
    } catch (err) {
      setError(err.message || 'Failed to upload document.')
    } finally {
      setLoadingUpload(false)
    }
  }

  async function handleAsk() {
    if (!question.trim()) {
      setError('Please enter a question.')
      return
    }

    setError('')
    setAnswer('')
    setResults([])
    setLoadingQuestion(true)

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      })

      if (!response.ok) {
        throw new Error(`Question failed with status ${response.status}`)
      }

      const data = await response.json()

      setAnswer(data.answer)
      setResults(data.results || [])
    } catch (err) {
      setError(err.message || 'Failed to get an answer.')
    } finally {
      setLoadingQuestion(false)
    }
  }

  return (
    <main className="app">
      <header className="header">
        <h1>DocuMind</h1>
        <p>Ask questions about your documents using RAG + AI.</p>
      </header>

      <section className="card">
        <h2>Upload Document</h2>

        <input
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={(event) => {
            setFile(event.target.files[0] || null)
            setUploadMessage('')
            setError('')
          }}
        />

        {file && (
          <p className="selected-file">
            Selected: <strong>{file.name}</strong>
          </p>
        )}

        <button
          type="button"
          onClick={handleUpload}
          disabled={!file || loadingUpload}
        >
          {loadingUpload ? 'Uploading...' : 'Upload'}
        </button>

        {uploadMessage && (
          <p className="success">{uploadMessage}</p>
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
          onClick={handleAsk}
          disabled={loadingQuestion}
        >
          {loadingQuestion ? 'Thinking...' : 'Ask Question'}
        </button>
      </section>

      {error && (
        <section className="card error">
          <strong>Error:</strong> {error}
        </section>
      )}

      {answer && (
        <section className="card">
          <h2>Answer</h2>

          <div className="answer">
            <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
        </section>
      )}

      {results.length > 0 && (
        <section className="card">
          <h2>Retrieved Sources</h2>

          <div className="sources">
            {results.map((result) => (
              <article className="source" key={result.chunk_id}>
                <div className="source-header">
                  <strong>Chunk {result.chunk_id}</strong>
                  <span>Page {result.page_number}</span>
                </div>

                <p className="score">
                  Score: {result.score.toFixed(3)}
                </p>

                <p>{result.text}</p>
              </article>
            ))}
          </div>
        </section>
      )}
    </main>
  )
}

export default App