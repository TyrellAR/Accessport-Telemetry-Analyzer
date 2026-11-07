import { useCallback, useEffect, useRef, useState } from "react";

import { getDatalogs } from "../api/datalogs";
import type { Datalog } from "../types/datalog";

export function useDatalogs() {
  const [datalogs, setDatalogs] = useState<Datalog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const controllerRef = useRef<AbortController | null>(null);

  const fetchDatalogs = useCallback(async () => {
    controllerRef.current?.abort();

    const controller = new AbortController();
    controllerRef.current = controller;

    try {
      const data = await getDatalogs(controller.signal);

      if (!controller.signal.aborted) {
        setDatalogs(data);
        setError(null);
      }
    } catch (err) {
      if (!controller.signal.aborted) {
        setError(
          err instanceof Error ? err.message : "Failed to load datalogs",
        );
      }
    } finally {
      if (!controller.signal.aborted) {
        setLoading(false);
      }
    }
  }, []);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);

    await fetchDatalogs();
  }, [fetchDatalogs]);

  useEffect(() => {
    const controller = new AbortController();

    controllerRef.current = controller;

    getDatalogs(controller.signal)
    .then((data) => {
      if(!controller.signal.aborted){
        setDatalogs(data);
      }
    })
    .catch((err: unknown) => {
      if (!controller.signal.aborted) {
        setError(
          err instanceof Error
          ? err.message
          : "Failed to load datalogs"
        );
      }
    })
    .finally(() => {
      if (!controller.signal.aborted) {
        setLoading(false);
      }
    });
    return () => {
      controller.abort();
    };
  }, []);

  return {
    datalogs,
    loading,
    error,
    refresh,
  };
}
