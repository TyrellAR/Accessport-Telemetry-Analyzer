
import { useEffect, useState } from "react";

import { getDatalogs } from "../api/datalogs";
import type { Datalog } from "../types/datalog";

export function useDatalogs() {
  const [datalogs, setDatalogs] = useState<Datalog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadDatalogs() {
      try {
        setLoading(true);
        setError(null);

        const data = await getDatalogs(controller.signal);
        setDatalogs(data);
      } catch (err) {
        if (controller.signal.aborted) {
          return;
        }

        setError(
          err instanceof Error
            ? err.message
            : "Failed to load datalogs"
        );
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    void loadDatalogs();

    return () => controller.abort();
  }, []);

  return { datalogs, loading, error };
}
