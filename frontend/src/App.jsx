import { useEffect, useMemo, useState } from "react";

const BIDDERS = ["BIDDER-ALPHA", "BIDDER-BRAVO", "BIDDER-CHARLIE", "BIDDER-DELTA"];
const REQUIRED = ["udyam", "gstn", "pan_it", "epfo_esic", "digilocker", "blacklist"];

async function api(url, options) {
  const response = await fetch(url, options);
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || body.detail || "Request failed");
  return body;
}
const Risk = ({ value }) => <span className={`badge risk-${value.toLowerCase()}`}>{value}</span>;
const Status = ({ value }) => <span className={`badge status-${value}`}>{value.replaceAll("_", " ")}</span>;

export default function App() {
  const [assessments, setAssessments] = useState([]);
  const [selectedId, setSelectedId] = useState();
  const [trail, setTrail] = useState([]);
  const [decision, setDecision] = useState();
  const [error, setError] = useState();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const selected = useMemo(() => assessments.find((item) => item.bidder_id === selectedId), [assessments, selectedId]);

  useEffect(() => {
    async function load() {
      try {
        const results = await Promise.all(BIDDERS.map((bidder_id) => api("/api/compliance/verify", {
          method: "POST", headers: { "content-type": "application/json" },
          body: JSON.stringify({ bidder_id, required_checks: REQUIRED }),
        })));
        setAssessments(results); setSelectedId(results[0].bidder_id);
      } catch (err) { setError(err.message); } finally { setLoading(false); }
    }
    load();
  }, []);

  useEffect(() => {
    if (!selectedId) return;
    api(`/api/audit/${selectedId}`).then(setTrail).catch((err) => setError(err.message));
  }, [selectedId, decision]);

  async function submitDecision(officer_decision) {
    try {
      setSaving(true); setError();
      const saved = await api("/api/audit/decision", {
        method: "POST", headers: { "content-type": "application/json" },
        body: JSON.stringify({ bidder_id: selectedId, decision: officer_decision, officer_id: "OFFICER-DEMO-001" }),
      });
      setDecision(saved);
    } catch (err) { setError(err.message); } finally { setSaving(false); }
  }

  const recorded = decision?.bidder_id === selectedId
    ? decision
    : trail.find((entry) => entry.timestamp === selected.audit_log_entry.timestamp);
  return <main className="app-shell">
    <header><div><p className="eyebrow">SIH 2026 · GeM procurement</p><h1>Bid Compliance Verification</h1></div><b>AI assesses evidence. Officers decide.</b></header>
    {error && <p className="error">{error}</p>}{loading && <p>Running live verification for all four demo bidders…</p>}
    <div className="layout">
      <aside><h2>Demo bidders</h2>{assessments.map((item) => <button className={`bidder ${selectedId === item.bidder_id ? "selected" : ""}`} onClick={() => { setSelectedId(item.bidder_id); setDecision(); }} key={item.bidder_id}><span>{item.bidder_id}</span><strong>{item.compliance_score}/100</strong><Risk value={item.risk_level} /></button>)}</aside>
      {selected && <section className="detail">
        <section className="title"><div><p className="eyebrow">AI assessment (immutable)</p><h2>{selected.bidder_id}</h2></div><div><strong className="score">{selected.compliance_score}</strong><Risk value={selected.risk_level} /></div></section>
        <section className="card"><h3>Verification checks</h3>{selected.checks.map((check) => <details key={check.source}><summary>{check.source}<Status value={check.status} /></summary><dl><div><dt>Confidence</dt><dd>{Math.round(check.confidence * 100)}%</dd></div><div><dt>Weight applied</dt><dd>{check.weight_applied}</dd></div><div><dt>Engine note</dt><dd>{check.note}</dd></div></dl></details>)}</section>
        <section className="card manual"><h3>Pending Manual Review</h3>{selected.pending_manual_review.length ? <ul>{selected.pending_manual_review.map((source) => <li key={source}>{source} requires manual verification</li>)}</ul> : <p>No source records require manual verification.</p>}</section>
        <section className="card"><h3>AI recommendations</h3><ul>{selected.recommendations.map((text) => <li key={text}>{text}</li>)}</ul></section>
        <section className="card"><p className="eyebrow">Procurement Officer action</p><h3>Record the final human decision</h3><div className="actions"><button disabled={saving} onClick={() => submitDecision("approve")}>Approve</button><button disabled={saving} className="reject" onClick={() => submitDecision("reject")}>Reject</button><button disabled={saving} className="more" onClick={() => submitDecision("request_more_info")}>Request More Info</button></div><div className="comparison"><div><span>AI assessment — unchanged</span><strong>{selected.compliance_score}/100 · <Risk value={selected.risk_level} /></strong></div><div><span>Officer decision</span><strong>{recorded?.officer_decision ? recorded.officer_decision.replaceAll("_", " ") : "Not recorded"}</strong>{recorded?.officer_id && <small>{recorded.officer_id}</small>}</div></div></section>
        <section className="card"><h3>Audit trail</h3><p>Every scoring run and separately recorded officer decision.</p><ol>{trail.map((entry) => <li key={entry._id}><time>{new Date(entry.timestamp).toLocaleString()}</time><span>AI: {entry.compliance_score}/100 · <Risk value={entry.risk_level} /></span><span>Officer: {entry.officer_decision ? `${entry.officer_decision.replaceAll("_", " ")} (${entry.officer_id})` : "not recorded"}</span></li>)}</ol></section>
      </section>}
    </div>
  </main>;
}
