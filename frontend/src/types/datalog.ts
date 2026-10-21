

export interface Datalog {
  id: number;
  filename: string;
  accessport_model: string | null;
  firmware_version: string | null;
  vehicle: string | null;
  reflash_tune: string | null;
  realtime_tune: string | null;
  created_at: string;
}

export interface TelemetrySample {
  timestamp: number;
  rpm: number | null;
  speed: number | null;
  coolant_temp: number | null;
  boost: number | null;
  boost_ext: number | null;
  afr: number | null;
  intake_temp: number | null;
  intake_temp_manifold: number | null;
  throttle_position: number | null;
  fuel_pressure: number | null;
  fuel_pressure_target: number | null;
  map: number | null;
  ignition_timing: number | null;
  inj_duty_cycle: number | null;
  inj_pulse_width: number | null;
  maf_corrected: number | null;
  load: number | null;
  oil_temp: number | null;
}

export interface MetricStatistics {
  minimum: number | null;
  maximum: number | null;
  average: number | null;
}

export interface TelemetryMetrics {
  boost: MetricStatistics;
  rpm: MetricStatistics;
  afr: MetricStatistics;
  coolant_temp: MetricStatistics;
}