import { useState } from "react";

import { uploadDatalog } from "../api/datalogs";
import type { Datalog } from "../types/datalog";

export function useUploadDatalog() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function upload(file: File): Promise<Datalog> {
    setUploading(true);
    setError(null);

    try {
      return await uploadDatalog(file);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to upload datalog");

      throw err;
    } finally {
      setUploading(false);
    }
  }

  return {
    upload,
    uploading,
    error,
  };
}
