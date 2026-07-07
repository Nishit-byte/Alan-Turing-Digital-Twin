from collections import defaultdict, deque

class ShortTermMemory:
    """
    In-memory 12-turn rolling buffer per session.
    NOTE: resets if the server restarts — long_term.py handles persistence.
    """
    def __init__(self, max_turns: int = 12):
        self.max_turns = max_turns
        self.buffers = defaultdict(lambda: deque(maxlen=max_turns))

    def add_turn(self, session_id: str, role: str, content: str):
        self.buffers[session_id].append({"role": role, "content": content})

    def get_history(self, session_id: str) -> list[dict]:
        return list(self.buffers[session_id])

    def get_history_string(self, session_id: str) -> str:
        turns = self.get_history(session_id)
        return "\n".join(f"{t['role'].upper()}: {t['content']}" for t in turns)

    def turn_count(self, session_id: str) -> int:
        return len(self.buffers[session_id])
    
    def clear_session(self, session_id: str):
        if session_id in self.buffers:
            del self.buffers[session_id]

# single shared instance used across the app
short_term_memory = ShortTermMemory(max_turns=12)