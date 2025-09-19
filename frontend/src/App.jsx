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

  const runMockPipeline = async () => {
    if (!file) return;
    setStatus("Processing ...");
    setResult(null);

    //Simulate backend 
    await new Promise((r) => setTimeout(r, 1000));

    const mockResponse = {
      latin_raw: "Hoc output tantum locum reservatum est.",
      english: "This output is just a placeholder"
    };

    setResult(mockResponse);
    setStatus("Done");
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
            <button className="primary" disabled={!file} onClick={runMockPipeline}>
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
