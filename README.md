# managejason

handle jason

## What this repo contains

- `messages.json` — a sample JSON file that contains chat messages as an array of objects. Each object should have at least `sender` and `text` fields (e.g. `{ "sender": "you", "text": "Hello" }`).
- `chat-view-fetch.html` — a simple static HTML page that fetches `messages.json` from the same folder and renders messages in a chat-like layout ("you"/left and "i"/right).

## Usage

1. Clone the repository:

```bash
git clone https://github.com/Jay-Bnk48/managejason.git
cd managejason
```

2. Serve the folder with a simple HTTP server (required because the HTML uses `fetch`):

- Python 3:

```bash
python -m http.server 8000
```

- Node (http-server):

```bash
npx http-server -p 8000
```

3. Open the chat viewer in your browser:

```
http://localhost:8000/chat-view-fetch.html
```

4. To use your own JSON file, replace `messages.json` with your file (same folder) or edit the existing file. The expected format is an array of message objects. Example:

```json
[
  { "sender": "you", "text": "Hello!", "time": "2026-01-29T12:00:00Z" },
  { "sender": "i",   "text": "Hi there!", "time": "2026-01-29T12:00:05Z" }
]
```

## Alternatives

- If you prefer not to run a server, use a local file-input version (file picker) that reads a JSON file via the browser File API. I can add that if you want.

## License

MIT
