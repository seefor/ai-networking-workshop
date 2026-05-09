# Bonus Lab: Bun Chat UI with Ollama + Memory

Build a real web-based chat interface in **~15 minutes** using [Bun](https://bun.sh) — a fast all-in-one JavaScript runtime with a built-in HTTP server and `fetch`. No npm install, no Express, no dependencies.

## What You'll Build

A browser chat UI that:
- Talks to your local Ollama model
- Remembers the full conversation (just like Lab 3's Python chatbot — but in a browser)
- Runs with a single command: `bun run server.js`

```
┌──────────────────────────────────┐
│  🤖 AI Chat  ·  Bun + Ollama    │   ← served at localhost:3000
├──────────────────────────────────┤
│                                  │
│   [assistant bubble]             │
│              [user bubble]  →    │
│   [assistant bubble]             │
│              [user bubble]  →    │
│                                  │
├──────────────────────────────────┤
│  [ type a message...  ] [Send]   │
└──────────────────────────────────┘
```

## Why Bun?

| Feature | Node.js | Bun |
|---|---|---|
| HTTP server | need Express/Fastify | **built-in** `Bun.serve()` |
| `fetch` | need axios/node-fetch | **built-in** |
| Start time | ~200ms | ~10ms |
| Install deps | `npm install` | nothing needed here |

## Prerequisites

Make sure Ollama is running:

```bash
ollama serve
ollama pull llama3.2:3b   # if you haven't already
```

Install Bun (one command):

```bash
curl -fsSL https://bun.sh/install | bash
```

Verify:

```bash
bun --version
```

## Lab Structure

```
bonus/lab-bun-chat/
├── server.js          ← You edit this (4 TODOs)
├── solution/
│   └── server.js      ← Peek if you get stuck
└── README.md
```

## Your Task — 4 TODOs

Open `server.js`. The HTTP server, chat UI, and routing are all pre-built. You fill in four blanks inside the `handleChat()` function:

### TODO 1 — Write your system prompt

Give your assistant a role. Tell it what network devices are available and how it should behave.

### TODO 2 — Remember the user's message

Push the incoming message onto `conversationHistory` so the model can see what was said before.

```js
conversationHistory.push({ role: "user", content: userMessage });
```

### TODO 3 — Call Ollama with the full history

Use the built-in `fetch()` to POST to Ollama's chat endpoint. Include the system prompt **plus** the entire `conversationHistory` as the `messages` array.

Ollama endpoint: `http://localhost:11434/api/chat`

Request body shape:
```json
{
  "model": "llama3.2:3b",
  "stream": false,
  "messages": [
    { "role": "system",    "content": "..." },
    { "role": "user",      "content": "first message" },
    { "role": "assistant", "content": "first reply" },
    { "role": "user",      "content": "second message" }
  ]
}
```

### TODO 4 — Extract the reply and save it

Ollama responds with:
```json
{ "message": { "role": "assistant", "content": "the reply" } }
```

Pull out `data.message.content`, push it to history, and return:
```js
return Response.json({ reply, historyLength: conversationHistory.length });
```

## Running It

```bash
cd bonus/lab-bun-chat
bun run server.js
```

Then open **http://localhost:3003** in your browser.

> The server starts immediately even with the TODOs empty. Until you complete them,
> the chat will respond with a `501` stub error — that's expected and intentional!

## Testing Memory

Send these messages in order — if memory works, the second answer will reference the first:

1. `"What is OSPF?"`
2. `"What did I just ask you?"`
3. `"Summarise our conversation so far"`

Watch the **memory: N msgs** badge in the header go up. Hit **Reset** to start fresh.

## Stretch Goals

Done early? Try these:

- **Change the model** — swap `llama3.2:3b` for `mistral` or `qwen2.5:3b`
- **Limit memory depth** — only send the last 10 messages to avoid context overflow
- **Add timestamps** — show when each message was sent
- **Stream responses** — set `stream: true` and use `ReadableStream` to show tokens as they arrive
- **Multiple personas** — add a dropdown to switch between different system prompts

## Key Concepts

**`Bun.serve()`** replaces Express. One object, handles everything:
```js
Bun.serve({
  port: 3000,
  fetch(req) {
    return new Response("hello");
  }
});
```

**Memory = an array you keep around.** The model itself is stateless — you're the one building context by sending the full history on every request.

**`fetch()` is built in.** No imports, no `axios`, just call it directly.
