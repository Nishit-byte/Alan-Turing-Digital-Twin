export default function MessageBubble({ role, content }) {
  const isUser = role === 'user';
  return (
    <div style={{ display: 'flex', justifyContent: isUser ? 'flex-end' : 'flex-start', marginBottom: 16 }}>
      <div style={{
        maxWidth: '72%',
        padding: '14px 18px',
        borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
        background: isUser
          ? 'linear-gradient(135deg, #8b3fd1, #e91e8c)'
          : 'var(--panel-raised)',
        border: isUser ? 'none' : '1px solid var(--border)',
        boxShadow: isUser ? '0 0 20px rgba(233,30,140,0.25)' : '0 0 16px rgba(77,127,255,0.1)',
        fontSize: '1.05rem',
        lineHeight: 1.5,
        whiteSpace: 'pre-wrap'
      }}>
        {!isUser && (
          <div className="display-font" style={{ fontSize: '0.65rem', color: 'var(--blue)', marginBottom: 6 }}>
            TURING
          </div>
        )}
        {content}
      </div>
    </div>
  );
}