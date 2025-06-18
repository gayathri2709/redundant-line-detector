import React, { useState } from "react";
import { FileUpload } from "primereact/fileupload";
import { Card } from "primereact/card";
import { ProgressSpinner } from "primereact/progressspinner";
import { DataView } from "primereact/dataview";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async ({ files }) => {
    const file = files[0];
    if (!file) return;

    const disallowed = [".jpg", ".jpeg", ".png", ".gif"];
    if (disallowed.some((ext) => file.name.toLowerCase().endsWith(ext))) {
      alert("Image files are not allowed.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/upload/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      console.error("Upload failed:", error);
    } finally {
      setLoading(false);
    }
  };

  const itemTemplate = (item) => {
    const indexes = Array.isArray(item.indexes)
      ? item.indexes
      : item.indexes
      ? [item.indexes]
      : [];
    return (
      <div className="p-2">
        <div>
          <code>{item.line}</code> — found at lines {indexes.join(", ")}
        </div>
      </div>
    );
  };
  return (
    <div className="p-5">
      <Card title="Redundant Line Detector">
        <FileUpload
          name="file"
          customUpload
          uploadHandler={handleUpload}
          accept=".py,.java,.txt,.log,.csv,.pdf,.sql"
          chooseLabel="Choose File"
          uploadLabel="Check"
          cancelLabel="Cancel"
        />

        {loading && (
          <div className="p-mt-4 text-center">
            <ProgressSpinner />
            <p>Processing file...</p>
          </div>
        )}

        {result && (
          <div className="mt-4">
            <h4>Redundant Lines Found</h4>
            <DataView
              value={Object.entries(result.redundant_lines || {}).map(([line, indexes]) => ({
              line,
               indexes,
                }))}
              itemTemplate={itemTemplate}
              layout="list"
            />
          </div>
        )}
      </Card>
    </div>
  );
}

export default App;
