
import { useDatalogs } from "../hooks/useDatalogs";

export default function Dashboard() {
  const { datalogs, loading, error } = useDatalogs();

  if (loading) {
    return <p>Loading datalogs...</p>;
  }

  if (error) {
    return <p role="alert">Error: {error}</p>;
  }

  return (
    <main>
      <h1>Accessport Telemetry Analyzer</h1>
      <h2>Datalogs</h2>

      {datalogs.length === 0 ? (
        <p>No datalogs uploaded yet.</p>
      ) : (
        <ul>
          {datalogs.map((datalog) => (
            <li key={datalog.id}>
              <strong>{datalog.filename}</strong>
              {" — "}
              {datalog.vehicle ?? "Unknown vehicle"}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
