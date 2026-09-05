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
        `Uploaded ${data.filename} — ${data.chunks} chunks created.`,
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

  function handleKeyDown(event) {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
      handleAsk()
    }
  }

  return (
    <div className="app-shell">

      {/* Background */}
      <div className="background-glow glow-one" />
      <div className="background-glow glow-two" />

      {/* Navigation */}
      <nav className="navbar">
        <div className="brand">
          <div className="brand-mark">
            D
          </div>

          <span>DocuMind</span>
        </div>

        <div className="nav-status">
          <span className="status-dot" />
          RAG Online
        </div>
      </nav>

      <main className="app-container">

        {/* Hero */}
        <header className="hero">
          <div className="hero-label">
            DOCUMENT INTELLIGENCE
          </div>

          <h1>
            Understand your
            <span> documents.</span>
          </h1>

          <p>
            Upload a document, ask a question, and let DocuMind
            find the answer using retrieval-augmented generation.
          </p>
        </header>

        {/* Upload */}
        <section className="card upload-card">

          <div className="card-header">
            <div>
              <span className="eyebrow">01 · KNOWLEDGE BASE</span>
              <h2>Add a document</h2>
              <p>
                Upload a PDF, TXT, or DOCX file to begin.
              </p>
            </div>

            <div className="header-icon">
              +
            </div>
          </div>

          <label className={`drop-zone ${file ? 'has-file' : ''}`}>

            <input
              type="file"
              accept=".pdf,.txt,.docx"
              onChange={(event) => {
                setFile(event.target.files[0] || null)
                setUploadMessage('')
                setError('')
              }}
            />

            <div className="upload-symbol">
              ↑
            </div>

            <div className="drop-content">
              <strong>
                {file ? file.name : 'Choose a document'}
              </strong>

              <span>
                {file
                  ? 'Ready to be processed'
                  : 'or drag and drop your file here'}
              </span>
            </div>

            <span className="file-types">
              PDF · TXT · DOCX
            </span>
          </label>

          {file && (
            <div className="selected-file">

              <div className="file-icon">
                {file.name.toLowerCase().endsWith('.pdf')
                  ? 'PDF'
                  : 'FILE'}
              </div>

              <div className="file-details">
                <span>Selected document</span>
                <strong>{file.name}</strong>
              </div>

              <button
                className="remove-file"
                type="button"
                onClick={() => {
                  setFile(null)
                  setUploadMessage('')
                }}
              >
                ×
              </button>
            </div>
          )}

          <button
            className="primary-button"
            type="button"
            onClick={handleUpload}
            disabled={!file || loadingUpload}
          >
            {loadingUpload ? (
              <>
                <span className="spinner" />
                Processing document...
              </>
            ) : (
              <>
                Upload & Process
                <span>→</span>
              </>
            )}
          </button>

          {uploadMessage && (
            <div className="success-message">
              <span className="message-icon">✓</span>
              <span>{uploadMessage}</span>
            </div>
          )}
        </section>

        {/* Ask */}
        <section className="card ask-card">

          <div className="card-header">
            <div>
              <span className="eyebrow">02 · ASK YOUR DOCUMENT</span>
              <h2>What would you like to know?</h2>
              <p>
                Ask questions naturally. DocuMind retrieves the
                most relevant parts of your document.
              </p>
            </div>

            <div className="header-icon">
              ?
            </div>
          </div>

          <div className="question-box">

            <textarea
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about your document..."
              rows={5}
            />

            <div className="question-footer">

              <span className="character-count">
                {question.length > 0
                  ? `${question.length} characters`
                  : 'Ctrl + Enter to submit'}
              </span>

              <button
                className="ask-button"
                type="button"
                onClick={handleAsk}
                disabled={loadingQuestion}
              >
                {loadingQuestion ? (
                  <>
                    <span className="spinner" />
                    Thinking...
                  </>
                ) : (
                  <>
                    Ask Question
                    <span>→</span>
                  </>
                )}
              </button>

            </div>
          </div>
        </section>

        {/* Error */}
        {error && (
          <section className="message-card error-message">
            <span className="message-icon">!</span>

            <div>
              <strong>Something went wrong</strong>
              <p>{error}</p>
            </div>
          </section>
        )}

        {/* Answer */}
        {answer && (
          <section className="card answer-card">

            <div className="result-header">

              <div>
                <span className="eyebrow">03 · GENERATED RESPONSE</span>
                <h2>Answer</h2>
              </div>

              <div className="ai-badge">
                <span className="status-dot" />
                AI
              </div>

            </div>

            <div className="answer-content">
              <ReactMarkdown>
                {answer}
              </ReactMarkdown>
            </div>

          </section>
        )}

        {/* Sources */}
        {results.length > 0 && (
          <section className="card sources-card">

            <div className="result-header">

              <div>
                <span className="eyebrow">04 · RAG RETRIEVAL</span>
                <h2>Retrieved sources</h2>
              </div>

              <span className="source-count">
                {results.length} sources
              </span>

            </div>

            <div className="sources">

              {results.map((result, index) => (
                <article
                  className="source"
                  key={result.chunk_id ?? index}
                >

                  <div className="source-top">

                    <div className="source-number">
                      {String(index + 1).padStart(2, '0')}
                    </div>

                    <div className="source-meta">
                      <strong>
                        Chunk {result.chunk_id}
                      </strong>

                      <span>
                        Page {result.page_number}
                      </span>
                    </div>

                    <div className="score">
                      {(result.score * 100).toFixed(1)}%
                      <small>match</small>
                    </div>

                  </div>

                  <p>
                    {result.text}
                  </p>

                </article>
              ))}

            </div>
          </section>
        )}

        {/* Footer */}
        <footer className="footer">
          <div className="footer-brand">
            <span className="footer-mark">D</span>
            DocuMind
          </div>

          <span>
            Retrieval-Augmented Generation
          </span>

          <span>
            •
          </span>

          <span>
            Vector Search
          </span>
        </footer>

      </main>
    </div>
  )
}

export default App