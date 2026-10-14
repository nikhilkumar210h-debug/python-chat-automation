# Progress Tracker

## Milestones

| Milestone | Task | Status |
|-----------|------|--------|
| M1 | Capture + Clipboard | ✅ Completed |
| M2 | Parse chat | ✅ Completed |
| M3 | Rule engine | ✅ Completed |
| M4 | Config + Logging + Errors | ✅ Completed |

---

## M2: Chat Parsing Details

- Format: `Sender: message` per line
- Line endings: `\r\n`
- Messages may contain `:` internally (e.g., "Rohan: time 5:30 hai")
- Solution: `split(":", 1)` to split only on first colon

---

## M3: Rule Engine Details

- Rules stored as list of dicts in `rules.py`
- Three match types: `exact`, `phrase`, `keyword`
- Cleaning: removes punctuation, lowercases, normalizes whitespace
- Returns: `{ "reason": str, "reply": str | None }`
- Handles: no messages, non-target sender, empty message, no match
- `AUTO_SEND` remains `False` (dry-run by default)

---

## M4: Config + Logging + Errors

**Config (`config.json`):**
- `target_user`: "nkm"
- `check_interval`: 5 seconds
- `auto_send`: false
- `ai_enabled`: true
- `ai_model`: "meta/llama-3.2-11b-vision-instruct"

**Logging (`logger.py`):**
- CSV at `data/chat_log.csv`
- Columns: timestamp, sender, message, reply, status
- Auto-creates directory, writes header on first run
- Handles PermissionError (file open in Excel)

**Error Handling (`app.py`):**
- Config file missing / invalid JSON / missing keys → clean exit with message
- KeyboardInterrupt → graceful stop
- General Exception → prints error, waits for Enter before closing browser

---

## AI Reply (`ai_reply.py`)

- Provider: NVIDIA API (OpenAI-compatible)
- Model: `meta/llama-3.2-11b-vision-instruct`
- Context: Last 10 messages (role: user/assistant)
- System prompt: Hinglish, max 15 words, no promises, no personal info
- Params: max_tokens=60, temperature=0.3, timeout=20s
- Returns None on API failure (bot continues)

---

## Current State

- ✅ All core milestones done
- ✅ Dry-run mode working (auto_send: false)
- ✅ Rule engine covers common greetings/phrases
- ✅ AI fallback integrated
- ✅ Logging persists every interaction
- ✅ Graceful shutdown on Ctrl+C

---

## Next Steps (Optional)

- [ ] Add more rules for common conversations
- [ ] Implement message deduplication by ID (already using `data-msg-id`)
- [ ] Add health check / heartbeat logging
- [ ] Support multiple target users
- [ ] Web dashboard for log viewing