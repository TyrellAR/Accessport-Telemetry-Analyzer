import { apiGet} from "./client";

import type {
  Datalog,
  TelemetrySample,
  TelemetryMetrics,
} from "../types/datalog";

export function getDatalogs(
  signal?: AbortSignal
): Promise<Datalog[]> {
  return apiGet<Datalog[]>("/logs", signal);
}

export function getDatalogById(
  id: number,
  signal?: AbortSignal
): Promise<Datalog> {
  return apiGet<Datalog>(`/logs/${id}`, signal);
}

export function getDatalogTelemetry(
  id: number,
  limit = 100,
  offset = 0,
  signal?: AbortSignal
): Promise<TelemetrySample[]> {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });

  return apiGet<TelemetrySample[]>(
    `/logs/${id}/telemetry?${params.toString()}`,
    signal
  );
}

export function getDatalogMetrics(
  id: number,
  signal?: AbortSignal
): Promise<TelemetryMetrics> {
  return apiGet<TelemetryMetrics>(
    `/logs/${id}/metrics`,
    signal
  );
}