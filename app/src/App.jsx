import { useEffect, useState } from "react";

const money = (value) => value || "-";

function Metric({ label, value }) {
  return (
    <div className="metric">
      <div className="metric-value">{value}</div>
      <div className="metric-label">{label}</div>
    </div>
  );
}

function BulletList({ items }) {
  if (!items?.length) return null;

  return (
    <ul className="detail-list">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

function CandidateCard({ candidate }) {
  const details = candidate.underwriting_details || {};

  return (
    <article className="card">
      <div className="card-top">
        <div>
          <h3>{candidate.name}</h3>
          <p className="muted">{candidate.industry}</p>
        </div>
        <span className={`pill pill-${candidate.priority || "medium"}`}>{candidate.priority || "n/a"}</span>
      </div>
      <div className="grid">
        <div>
          <span className="label">Location</span>
          <span>{candidate.location}</span>
        </div>
        <div>
          <span className="label">Years</span>
          <span>{candidate.years_in_business}</span>
        </div>
        <div>
          <span className="label">Revenue</span>
          <span>{money(candidate.revenue)}</span>
        </div>
        <div>
          <span className="label">Cash Flow</span>
          <span>{money(candidate.cash_flow)}</span>
        </div>
        <div>
          <span className="label">Status</span>
          <span>{candidate.status}</span>
        </div>
        <div>
          <span className="label">Retiring Owner</span>
          <span>{candidate.retiring_owner_status}</span>
        </div>
      </div>
      <p className="notes">{candidate.notes}</p>
      <div className="footer">
        <span>Underwriting: {candidate.underwriting_status || "pending"} ({candidate.underwriting_score || "-"})</span>
        <span>Research: {candidate.research_status || "pending"} ({candidate.research_score || "-"})</span>
      </div>
      <details className="details-panel">
        <summary>Underwriting details</summary>
        <div className="details-body">
          <div className="details-grid">
            <div>
              <span className="label">Bestimate</span>
              <span>{money(candidate.bestimate)}</span>
            </div>
            <div>
              <span className="label">Recurring Revenue</span>
              <span>{candidate.recurring_revenue_signal || "-"}</span>
            </div>
            <div>
              <span className="label">Team Signal</span>
              <span>{candidate.team_signal || "-"}</span>
            </div>
          </div>

          {details.why_it_fits ? (
            <div className="detail-section">
              <span className="label">Why It Fits</span>
              <p>{details.why_it_fits}</p>
            </div>
          ) : null}

          {details.key_risks ? (
            <div className="detail-section">
              <span className="label">Key Risks</span>
              <p>{details.key_risks}</p>
            </div>
          ) : null}

          <div className="detail-section">
            <span className="label">Financing View</span>
            <BulletList items={details.financing_view} />
          </div>

          <div className="detail-section">
            <span className="label">Missing Facts</span>
            <BulletList items={details.missing_facts} />
          </div>

          <div className="detail-section">
            <span className="label">Preliminary Verdict</span>
            <BulletList items={details.preliminary_verdict} />
          </div>
        </div>
      </details>
      {candidate.website ? (
        <a className="site-link" href={candidate.website} target="_blank" rel="noreferrer">
          Open site
        </a>
      ) : null}
    </article>
  );
}

export default function App() {
  const [data, setData] = useState(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    const dashboardUrl = `${import.meta.env.BASE_URL}data/dashboard.json`;

    fetch(dashboardUrl)
      .then((res) => res.json())
      .then(setData)
      .catch(() => setData({ summary: {}, candidates: [] }));
  }, []);

  const candidates = (data?.candidates || []).filter((candidate) => {
    const haystack = [
      candidate.name,
      candidate.industry,
      candidate.location,
      candidate.status,
      candidate.priority
    ]
      .join(" ")
      .toLowerCase();
    return haystack.includes(query.toLowerCase());
  });

  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">DC Acquisition Pipeline</p>
        <h1>Business prospects worth buying</h1>
        <p className="hero-copy">
          Daily sourced, underwritten, researched, and ranked against the active buy box.
        </p>
        <input
          className="search"
          type="search"
          placeholder="Search by name, industry, or location"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </section>

      <section className="metrics">
        <Metric label="Total Prospects" value={data?.summary?.total ?? 0} />
        <Metric label="Qualified" value={data?.summary?.qualified ?? 0} />
        <Metric label="High Priority" value={data?.summary?.highPriority ?? 0} />
        <Metric label="Underwriting Pending" value={data?.summary?.underwritingPending ?? 0} />
        <Metric label="Research Pending" value={data?.summary?.researchPending ?? 0} />
      </section>

      <section className="list">
        {candidates.map((candidate) => (
          <CandidateCard key={`${candidate.name}-${candidate.location}`} candidate={candidate} />
        ))}
      </section>
    </main>
  );
}
