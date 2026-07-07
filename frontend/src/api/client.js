const BASE_URL = 'http://127.0.0.1:8000';

export async function sendMessage(sessionId, question) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, question })
  });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}