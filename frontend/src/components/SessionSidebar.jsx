import { useEffect, useState } from 'react';

const BASE_URL = 'http://127.0.0.1:8000';

export default function SessionSidebar({ currentSessionId, onSelectSession, onNewChat, onSessionDeleted }) {
  const [sessions, setSessions] = useState([]);

  const loadSessions = async () => {
    try {
      const res = await fetch(`${BASE_URL}/sessions`);
      const data = await res.json();
      setSessions(data);
    } catch (err) {
      console.error('Failed to load sessions', err);
    }
  };

  useEffect(() => {
    loadSessions();
  }, [currentSessionId]);

  const handleDelete = async (e, sessionId) => {
    e.stopPropagation(); // don't trigger onSelectSession
    if (!confirm('Delete this conversation? This cannot be undone.')) return;

    try {
      await fetch(`${BASE_URL}/sessions/${sessionId}`, { method: 'DELETE' });
      setSessions(prev => prev.filter(s => s.session_id !== sessionId));
      if (sessionId === currentSessionId) {
        onSessionDeleted();
      }
    } catch (err) {
      console.error('Failed to delete session', err);
    }
  };

  return (
    <div style={{
      width: 260, height: '100vh', background: 'var(--panel)',
      borderRight: '1px solid var(--border)', padding: 20,
      position: 'fixed', left: 0, top: 0, zIndex: 5, overflowY: 'auto'
    }}>
      <div className="display-font" style={{ fontSize: '0.85rem', color: 'var(--magenta)', marginBottom: 20 }}>
        SESSIONS
      </div>

      <button
        onClick={onNewChat}
        style={{
          width: '100%', padding: '10px 14px', marginBottom: 20,
          background: 'linear-gradient(135deg, #8b3fd1, #e91e8c)',
          border: 'none', borderRadius: 10, color: 'white', cursor: 'pointer',
          fontFamily: 'Orbitron', fontSize: '0.7rem', letterSpacing: '0.05em'
        }}
      >
        + NEW CHAT
      </button>

      {sessions.length === 0 && (
        <div style={{ color: 'var(--text-dim)', fontSize: '0.85rem' }}>No conversations yet.</div>
      )}

      {sessions.map(s => (
        <div
          key={s.session_id}
          onClick={() => onSelectSession(s.session_id)}
          style={{
            display: 'flex', justifyContent: 'space-between', alignItems: 'center',
            padding: '10px 12px', marginBottom: 8, borderRadius: 8, cursor: 'pointer',
            background: s.session_id === currentSessionId ? 'var(--panel-raised)' : 'transparent',
            border: s.session_id === currentSessionId ? '1px solid var(--border)' : '1px solid transparent',
            fontSize: '0.85rem', color: 'var(--text)'
          }}
        >
          <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>
            {s.title || 'Untitled conversation'}
          </span>
          <span
            onClick={(e) => handleDelete(e, s.session_id)}
            style={{ color: 'var(--text-dim)', marginLeft: 8, cursor: 'pointer', fontSize: '0.9rem' }}
            title="Delete conversation"
          >
            🗑
          </span>
        </div>
      ))}
    </div>
  );
}