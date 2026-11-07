import { useRef, useState } from "react";

import { useDatalogs } from "../hooks/useDatalogs";
import { useUploadDatalog } from "../hooks/useUploadDatalog";

export default function Dashboard() {
  const { datalogs, loading, error, refresh } = useDatalogs();

  const { upload, uploading, error: uploadError } = useUploadDatalog();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  async function handleUpload(event: React.SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile || uploading) {
      return;
    }

    setUploadSuccess(false);

    try {
      await upload(selectedFile);
      await refresh();

      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
      
      setUploadSuccess(true);
    } catch (err) {
      console.error("Failed to upload datalog:", err);
    }
  } // Closes handleUpload

  return (
    <main>
      <h1>Accessport Telemetry Analyzer</h1>

      <section>
        <h2>Upload Datalog</h2>

        <form onSubmit={handleUpload}>
          <input
          ref={fileInputRef}
            type="file"
            accept=".csv,text/csv"
            onChange={(event) => {
              setSelectedFile(event.target.files?.[0] ?? null);
              setUploadSuccess(false);
            }}
          />

          <button type="submit" disabled={!selectedFile || uploading}>
            {uploading ? "Uploading..." : "Upload CSV"}
          </button>
        </form>
        {uploadError && <p role="alert">Upload error: {uploadError}</p>}

        {uploadSuccess && <p role="status">Datalog uploaded successfully.</p>}
      </section>

      <section>
        <h2>Datalogs</h2>

        {loading ? (
          <p>Loading datalogs...</p>
        ) : error ? (
          <p role="alert">Error: {error}</p>
        ) : datalogs.length === 0 ? (
          <p>No datalogs uploaded yet.</p>
        ) : (
          <ul>
            {datalogs.map((datalog) => (
              <li key={datalog.id}>
                <strong>{datalog.filename}</strong>
                {" - "}
                {datalog.vehicle ?? "Unknown vehicle"}
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
