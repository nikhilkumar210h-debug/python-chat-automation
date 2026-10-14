# Chat Automation Bot

Automated chat bot for `trio-day.trioday-nikhil.workers.dev/chat` using Playwright + rule engine + AI fallback.

## Features

- **Browser Automation**: Uses Playwright with persistent Brave profile (keeps login session)
- **Rule Engine**: Exact/phrase/keyword matching for instant replies
- **AI Fallback**: NVIDIA Llama-3.2-11B for unmatched messages (Hinglish, short replies)
- **Config-driven**: All settings in `config.json`
- **Logging**: CSV logs in `data/chat_log.csv`
- **Dry-run Mode**: Test without sending messages

## Project Structure

```
chat_automation/
├── app.py              # Main entry point
├── ai_reply.py         # AI reply via NVIDIA API
├── rules.py            # Rule engine (exact/phrase/keyword)
├── logger.py           # CSV logging
├── config.json         # Configuration
├── data/
│   ├── chat_log.csv    # Auto-generated logs
│   └── sample_chat.txt # Sample chat format
└── README.md
```

## Prerequisites

- Python 3.10+
- Brave Browser installed at `C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe`
- NVIDIA API key in environment variable `NVIDIA_API_KEY`

## Installation

```bash
pip install playwright openai python-dotenv
playwright install chromium
```

## Configuration

Edit `config.json`:

```json
{
  "target_user": "nkm",
  "check_interval": 5,
  "auto_send": false,
  "ai_enabled": true,
  "ai_model": "meta/llama-3.2-11b-vision-instruct"
}
```

| Key | Description |
|-----|-------------|
| `target_user` | Username to monitor/reply to |
| `check_interval` | Seconds between checks |
| `auto_send` | `false` = dry-run (logs only), `true` = sends replies |
| `ai_enabled` | Enable AI fallback when no rule matches |
| `ai_model` | NVIDIA model to use |

## Usage

```bash
python app.py
```

- Opens Brave with persistent profile (`C:\brave_profile`)
- Navigates to chat page
- Clicks target user's chat
- Monitors for new messages from target user
- Replies via rules first, then AI if enabled
- Logs every event to `data/chat_log.csv`

## Rule Engine

Rules defined in `rules.py` - supports three types:

- **exact**: Exact match after cleaning (punctuation removed, lowercase)
- **phrase**: Substring match
- **keyword**: Word boundary match

Example rule:
```python
{
    "name": "greeting",
    "type": "phrase",
    "trigger": ["hello", "hi", "hey"],
    "reply": "Hii bhai!"
}
```

## AI Reply

When no rule matches and `ai_enabled: true`:
- Sends last 10 messages to NVIDIA Llama-3.2-11B
- System prompt enforces: Hinglish, 1 short line, no promises, no personal info
- Temperature 0.3 for consistent replies

## Logging

Each event logged to `data/chat_log.csv`:

| Column | Description |
|--------|-------------|
| timestamp | ISO format datetime |
| sender | `target_user` or `me` |
| message | Incoming message text |
| reply | Bot's reply (or empty) |
| status | `sent`, `dry-run`, `no_reply` |

## Stopping

Press `Ctrl+C` to stop gracefully.

## Notes

- Requires existing Brave profile with logged-in session
- Selectors target specific DOM structure of the chat site
- `auto_send: false` recommended for testing
- AI needs `NVIDIA_API_KEY` in environment