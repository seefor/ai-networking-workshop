// ============================================================
// Bonus Lab — SOLUTION: Bun Chat UI with Ollama + Memory
// ============================================================

const OLLAMA_URL = "http://localhost:11434";
const MODEL = "llama3.2:3b";
const PORT = 3000;

// ─────────────────────────────────────────────────────────────
// SOLUTION TODO 1: System prompt
// ─────────────────────────────────────────────────────────────
const SYSTEM_PROMPT = `You are a network engineer assistant.

Available devices in this lab:
- spine1, spine2 (core switches, 192.168.0.11/12)
- leaf1, leaf2   (access switches, 192.168.0.21/22)

Keep answers concise and practical. When troubleshooting,
suggest specific commands the engineer could run.`;


// Conversation memory
const conversationHistory = [];


async function handleChat(req) {
  let body;
  try {
    body = await req.json();
  } catch {
    return Response.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const userMessage = body.message?.trim();
  if (!userMessage) {
    return Response.json({ error: "No message provided" }, { status: 400 });
  }

  // ─────────────────────────────────────────────────────────
  // SOLUTION TODO 2: Remember what the user said
  // ─────────────────────────────────────────────────────────
  conversationHistory.push({ role: "user", content: userMessage });

  // ─────────────────────────────────────────────────────────
  // SOLUTION TODO 3: Call Ollama with full conversation history
  // ─────────────────────────────────────────────────────────
  const ollamaRes = await fetch(`${OLLAMA_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: MODEL,
      stream: false,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        ...conversationHistory,
      ],
    }),
  });

  const data = await ollamaRes.json();

  // ─────────────────────────────────────────────────────────
  // SOLUTION TODO 4: Extract reply, save it, return it
  // ─────────────────────────────────────────────────────────
  const reply = data.message?.content ?? "No response from model.";
  conversationHistory.push({ role: "assistant", content: reply });

  return Response.json({ reply, historyLength: conversationHistory.length });
}


// ─────────────────────────────────────────────────────────────
// Bun HTTP server — auto-finds a free port starting from PORT
// ─────────────────────────────────────────────────────────────
const handler = {
  async fetch(req) {
    const { pathname } = new URL(req.url);

    if (pathname === "/" && req.method === "GET") {
      return new Response(HTML, {
        headers: { "Content-Type": "text/html; charset=utf-8" },
      });
    }

    if (pathname === "/api/chat" && req.method === "POST") {
      try {
        return await handleChat(req);
      } catch (err) {
        const msg = err.message?.includes("ECONNREFUSED")
          ? "Cannot reach Ollama — is it running? Try: ollama serve"
          : `Server error: ${err.message}`;
        return Response.json({ error: msg }, { status: 500 });
      }
    }

    if (pathname === "/api/reset" && req.method === "POST") {
      conversationHistory.length = 0;
      return Response.json({ ok: true });
    }

    return new Response("Not Found", { status: 404 });
  },
};

let server;
let port = PORT;
while (true) {
  try {
    server = Bun.serve({ port, ...handler });
    break;
  } catch (err) {
    if (err.code === "EADDRINUSE") {
      console.warn(`⚠️  Port ${port} is in use, trying ${port + 1}…`);
      port++;
    } else {
      throw err;
    }
  }
}

console.log(`\n🚀 Chat server running  →  http://localhost:${server.port}`);
console.log(`🤖 Model: ${MODEL}`);
console.log(`📡 Ollama: ${OLLAMA_URL}\n`);


// ─────────────────────────────────────────────────────────────
// Chat UI HTML (same as guided version)
// ─────────────────────────────────────────────────────────────
const HTML = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Chat — Bun + Ollama</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #0f1117;
    color: #e2e8f0;
    height: 100dvh;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  header {
    width: 100%;
    max-width: 760px;
    padding: 18px 24px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #1e2535;
  }

  header h1 { font-size: 1rem; font-weight: 600; color: #94a3b8; letter-spacing: 0.02em; }

  .badge {
    font-size: 0.72rem;
    background: #1e2535;
    border: 1px solid #2d3748;
    border-radius: 999px;
    padding: 3px 10px;
    color: #64748b;
  }
  .badge span { color: #38bdf8; font-weight: 700; }

  #messages {
    flex: 1;
    width: 100%;
    max-width: 760px;
    overflow-y: auto;
    padding: 24px 24px 8px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    scroll-behavior: smooth;
  }

  .msg {
    max-width: 82%;
    line-height: 1.6;
    padding: 12px 16px;
    border-radius: 14px;
    font-size: 0.92rem;
    white-space: pre-wrap;
    word-break: break-word;
    animation: fadeIn 0.15s ease;
  }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; } }

  .msg.user {
    align-self: flex-end;
    background: #1d4ed8;
    color: #eff6ff;
    border-bottom-right-radius: 4px;
  }

  .msg.assistant {
    align-self: flex-start;
    background: #1e2535;
    color: #e2e8f0;
    border-bottom-left-radius: 4px;
    border: 1px solid #2d3748;
  }

  .msg.error {
    align-self: flex-start;
    background: #450a0a;
    color: #fca5a5;
    border: 1px solid #7f1d1d;
    border-bottom-left-radius: 4px;
    font-size: 0.85rem;
  }

  .typing {
    align-self: flex-start;
    background: #1e2535;
    border: 1px solid #2d3748;
    border-radius: 14px;
    border-bottom-left-radius: 4px;
    padding: 14px 18px;
    display: flex;
    gap: 5px;
    align-items: center;
  }
  .typing span {
    width: 7px; height: 7px;
    background: #475569;
    border-radius: 50%;
    animation: bounce 1.2s infinite ease-in-out;
  }
  .typing span:nth-child(2) { animation-delay: 0.2s; }
  .typing span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-6px); background: #38bdf8; }
  }

  footer {
    width: 100%;
    max-width: 760px;
    padding: 12px 24px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .input-row { display: flex; gap: 8px; }

  #input {
    flex: 1;
    background: #1e2535;
    border: 1px solid #2d3748;
    border-radius: 10px;
    color: #e2e8f0;
    font-size: 0.92rem;
    padding: 12px 16px;
    outline: none;
    transition: border-color 0.15s;
    resize: none;
    height: 48px;
    max-height: 160px;
    overflow-y: auto;
    font-family: inherit;
    line-height: 1.5;
  }
  #input:focus { border-color: #3b82f6; }
  #input::placeholder { color: #475569; }

  button {
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-size: 0.85rem;
    font-weight: 600;
    padding: 0 18px;
    height: 48px;
    transition: opacity 0.15s, transform 0.1s;
  }
  button:active { transform: scale(0.97); }
  button:disabled { opacity: 0.4; cursor: not-allowed; }

  #send-btn { background: #2563eb; color: #fff; min-width: 80px; }
  #send-btn:hover:not(:disabled) { background: #1d4ed8; }

  #reset-btn {
    background: #1e2535;
    color: #64748b;
    border: 1px solid #2d3748;
    min-width: 70px;
  }
  #reset-btn:hover:not(:disabled) { color: #94a3b8; border-color: #475569; }

  .hint { text-align: center; font-size: 0.72rem; color: #334155; }
</style>
</head>
<body>

<header>
  <h1>🤖 AI Chat &nbsp;·&nbsp; Bun + Ollama</h1>
  <div class="badge">memory: <span id="count">0</span> msgs</div>
</header>

<div id="messages">
  <div class="msg assistant">👋 Hey! I'm your AI assistant running locally via Ollama.<br>Ask me anything — I'll remember this whole conversation.</div>
</div>

<footer>
  <div class="input-row">
    <textarea id="input" placeholder="Type a message… (Enter to send, Shift+Enter for new line)" rows="1"></textarea>
    <button id="send-btn">Send</button>
    <button id="reset-btn" title="Clear conversation">Reset</button>
  </div>
  <div class="hint">Running on Bun &nbsp;·&nbsp; Model: <strong style="color:#475569">${MODEL}</strong></div>
</footer>

<script>
  const messagesEl = document.getElementById('messages');
  const inputEl    = document.getElementById('input');
  const sendBtn    = document.getElementById('send-btn');
  const resetBtn   = document.getElementById('reset-btn');
  const countEl    = document.getElementById('count');

  function addMessage(role, text) {
    const div = document.createElement('div');
    div.className = 'msg ' + role;
    div.textContent = text;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return div;
  }

  function showTyping() {
    const el = document.createElement('div');
    el.className = 'typing';
    el.innerHTML = '<span></span><span></span><span></span>';
    messagesEl.appendChild(el);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return el;
  }

  inputEl.addEventListener('input', () => {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 160) + 'px';
  });

  async function sendMessage() {
    const text = inputEl.value.trim();
    if (!text) return;

    inputEl.value = '';
    inputEl.style.height = '48px';
    sendBtn.disabled = true;
    resetBtn.disabled = true;

    addMessage('user', text);
    const typing = showTyping();

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });
      const data = await res.json();
      typing.remove();

      if (data.error) {
        addMessage('error', '⚠️ ' + data.error);
      } else {
        addMessage('assistant', data.reply);
        countEl.textContent = data.historyLength ?? '?';
      }
    } catch (err) {
      typing.remove();
      addMessage('error', '⚠️ Network error: ' + err.message);
    } finally {
      sendBtn.disabled = false;
      resetBtn.disabled = false;
      inputEl.focus();
    }
  }

  sendBtn.addEventListener('click', sendMessage);

  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  resetBtn.addEventListener('click', async () => {
    await fetch('/api/reset', { method: 'POST' });
    messagesEl.innerHTML = '';
    countEl.textContent = '0';
    addMessage('assistant', '🔄 Conversation reset. Fresh start!');
  });

  inputEl.focus();
</script>
</body>
</html>`;
