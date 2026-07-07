export default function ReasoningTracePanel({ trace, overallConfidence, onClose }) {
  return (
    <div style={{
      position: 'fixed', top: 0, right: 0, height: '100vh', width: 340,
      background: 'var(--panel)', borderLeft: '1px solid var(--border)',
      padding: 20, overflowY: 'auto', zIndex: 10,
      boxShadow: '-10px 0 30px rgba(0,0,0,0.5)'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <span className="display-font" style={{ fontSize: '0.9rem', color: 'var(--magenta)' }}>REASONING TRACE</span>
        <button onClick={onClose} style={{
          background: 'none', border: 'none', color: 'var(--text-dim)', cursor: 'pointer', fontSize: '1.2rem'
        }}>✕</button>
      </div>

      <div style={{ marginBottom: 24 }}>
        <div className="mono-font" style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: 6 }}>
          OVERALL CONFIDENCE
        </div>
        <div style={{ height: 8, background: 'rgba(255,255,255,0.08)', borderRadius: 4, overflow: 'hidden' }}>
          <div style={{
            width: `${overallConfidence * 100}%`, height: '100%',
            background: 'linear-gradient(90deg, var(--blue), var(--magenta))'
          }} />
        </div>
        <div className="mono-font" style={{ fontSize: '0.8rem', color: 'var(--text)', marginTop: 4 }}>
          {(overallConfidence * 100).toFixed(1)}%
        </div>
      </div>

      {trace.map((step) => (
        <div key={step.step} style={{
          marginBottom: 16, padding: 12, background: 'var(--panel-raised)',
          borderRadius: 8, border: '1px solid var(--border)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
            <span className="mono-font" style={{ fontSize: '0.7rem', color: 'var(--blue)' }}>
              STEP {step.step}
            </span>
            <span className="mono-font" style={{ fontSize: '0.7rem', color: 'var(--magenta)' }}>
              {(step.confidence * 100).toFixed(0)}%
            </span>
          </div>
          <div style={{ fontSize: '0.85rem', color: 'var(--text-dim)', lineHeight: 1.4 }}>
            {step.source_excerpt}
          </div>
        </div>
      ))}
    </div>
  );
}