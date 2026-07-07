import { useState, useRef, useEffect } from 'react';
import MessageBubble from './components/MessageBubble';
import ReasoningTracePanel from './components/ReasoningTracePanel';
import CircuitCorner from './components/CircuitCorner';
import GradientWisp from './components/GradientWisp';
import SessionSidebar from './components/SessionSidebar';
import { sendMessage } from './api/client';

function generateSessionId() {
  return 'session-' + Math.random().toString(36).slice(2, 10);
}

export default function App() {
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem('turing_current_session') || generateSessionId();
  });
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [trace, setTrace] = useState(null);
  const [showTrace, setShowTrace] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    localStorage.setItem('turing_current_session', sessionId);
    loadHistory(sessionId);
  }, [sessionId]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadHistory = async (sid) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/sessions/${sid}/messages`);
      const data = await res.json();
      setMessages(data);
    } catch {
      setMessages([]);
    }
  };

  const handleNewChat = () => {
    const newId = generateSessionId();
    setSessionId(newId);
    setMessages([]);
    setTrace(null);
  };

  const handleSelectSession = (sid) => {
    setSessionId(sid);
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;
    const question = input.trim();
    setMessages(prev => [...prev, { role: 'user', content: question }]);
    setInput('');
    setLoading(true);

    try {
      const data = await sendMessage(sessionId, question);
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
      setTrace({ steps: data.reasoning_trace, overallConfidence: data.overall_confidence });
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: `[Connection error: ${err.message}]` }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', position: 'relative' }}>
      <GradientWisp />
      <CircuitCorner position="top-right" />
      <CircuitCorner position="bottom-left" />

      <SessionSidebar
        currentSessionId={sessionId}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        onSessionDeleted={handleNewChat}
      />

      <div style={{ marginLeft: 260 }}>
        <div style={{
          display: 'flex', justifyContent: 'center', gap: 48,
          padding: '24px 0', position: 'relative', zIndex: 2
        }}>
          <span className="display-font" style={{ fontSize: '0.8rem', color: 'var(--text)' }}>SESSION</span>
          <span
            className="display-font"
            style={{ fontSize: '0.8rem', color: showTrace ? 'var(--magenta)' : 'var(--text-dim)', cursor: 'pointer' }}
            onClick={() => setShowTrace(v => !v)}
          >
            TRACE
          </span>
          <span className="display-font" style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>ABOUT</span>
        </div>

        {messages.length === 0 && (
          <div style={{ textAlign: 'center', marginTop: 60, position: 'relative', zIndex: 2 }}>
            <h1 className="display-font" style={{ fontSize: '3.5rem', margin: 0, lineHeight: 1.1 }}>
              ALAN<br />TURING
            </h1>
            <p style={{ color: 'var(--text-dim)', fontSize: '1.1rem', marginTop: 12 }}>
              A digital twin grounded in his own writing
            </p>
          </div>
        )}

        <div style={{
          maxWidth: 720, margin: '0 auto', padding: '20px 24px 140px',
          position: 'relative', zIndex: 2
        }}>
          {messages.map((m, i) => <MessageBubble key={i} role={m.role} content={m.content} />)}
          {loading && (
            <div style={{ color: 'var(--text-dim)', fontSize: '0.9rem' }} className="mono-font">
              Turing is composing a reply...
            </div>
          )}
          <div ref={scrollRef} />
        </div>

        <div style={{
          position: 'fixed', bottom: 0, left: 260, right: 0,
          background: 'linear-gradient(to top, var(--void) 60%, transparent)',
          padding: '30px 24px 24px', zIndex: 5
        }}>
          <div style={{
            maxWidth: 720, margin: '0 auto', display: 'flex', gap: 10,
            background: 'var(--panel)', border: '1px solid var(--border)',
            borderRadius: 30, padding: '6px 6px 6px 20px'
          }}>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSend()}
              placeholder="Ask Turing something..."
              style={{
                flex: 1, background: 'none', border: 'none', outline: 'none',
                color: 'var(--text)', fontSize: '1rem', fontFamily: 'Rajdhani'
              }}
            />
            <button
              onClick={handleSend}
              style={{
                background: 'linear-gradient(135deg, #8b3fd1, #e91e8c)',
                border: 'none', borderRadius: 24, color: 'white', padding: '10px 22px',
                cursor: 'pointer', fontFamily: 'Orbitron', fontSize: '0.75rem', letterSpacing: '0.05em'
              }}
            >
              SEND
            </button>
          </div>
        </div>
      </div>

      {showTrace && trace && (
        <ReasoningTracePanel
          trace={trace.steps}
          overallConfidence={trace.overallConfidence}
          onClose={() => setShowTrace(false)}
        />
      )}
    </div>
  );
}