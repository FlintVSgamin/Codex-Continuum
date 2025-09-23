import { useState, useCallback } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [status, setStatus] = useState("");
  const [result, setResult] = useState(null);

  //Drag & drop 
  const onDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer?.files?.[0];
    if (f) setFile(f);
  }, []);

  //File selection 
  const onSelect = (e) => {
    const f = e.target.files?.[0];
    if (f) setFile(f);
  };

  //Backend call
  const runPipeline = async () => {
    if (!file) return;
    setStatus("Processing ...");
    setResult(null);

    const fd = new FormData();
    fd.append("file", file);
    fd.append("psm", "6");
    fd.append("lang", "lat");
    fd.append("engine", "tesseract");

    try {
      const resp = await fetch("http://localhost:8000/ocr", {
        method: "POST",
        body: fd,
      });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();
      setResult({
        latin_raw: data.latin ?? data.text ?? "",
        english: data.english ?? "",
      });
      setStatus("Done");
    } catch (err) {setStatus(`Error: ${err.message}`);}
  };

  const isLoading = typeof status === "string" && status.toLowerCase().startsWith("processing");
  return (
    <div className="container">
      <h1>Latin OCR → Translation (OCR)</h1>

      <div className="main-grid">
        {/* LEFT COLUMN — Upload + Controls */}
        <div className="upload-panel">
          <div
            className={`dropzone ${dragOver ? "over" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={onDrop}
          >
            <p>Drag & drop an image/PDF here</p>
            <p>or</p>
            <label className="btn">
              Choose file
              <input type="file" accept=".png,.jpg,.jpeg,.pdf" onChange={onSelect} hidden />
            </label>
          </div>

          {file && (
            <div className="filecard">
              <strong>Selected:</strong> {file.name} ({Math.round(file.size / 1024)} KB)
            </div>
          )}

          <div className="actions">
            <button className="primary" disabled={!file} onClick={runPipeline}>
              Run
            </button>
            <span className="status">{status}</span>
            {isLoading && (
              <div className="progress" role="status" aria-live="polite" aria-label="Processing">
                <div className="progress-bar" />
              </div>
            )}
          </div>
        </div>

        {/* RIGHT COLUMN — Output */}
        <div className="output-panel">
          <h2>Results</h2>
          {!result && (
            <p className="placeholder">Results will appear here.</p>
          )}
          {result && (
            <div className="results">
              <p><b>Latin (raw):</b> {result.latin_raw}</p>
              <p><b>English:</b> {result.english}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
