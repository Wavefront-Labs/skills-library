---
id: computing-software.ai-ml-engineering.open-webui.reset-admin-password-in-database
name: reset-admin-password-in-database
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [troubleshooting, password-reset, bcrypt, sqlite, docker, open-webui]
level: practitioner
status: docs-checked
description: "Reset a locked-out Open WebUI admin password by writing a bcrypt hash into the auth table of webui.db for Docker or local installs."
sources:
  - https://docs.openwebui.com/troubleshooting/password-reset
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: regain admin access when the password is lost (SQLite database `webui.db`).

## 1. Generate a bcrypt hash
```bash
htpasswd -bnBC 10 "" your-new-password | tr -d ':\n'
```
In the one-line Docker command below, every `$` in the hash must be triple-escaped.

## 2a. Docker, reliable step-by-step method
```bash
docker run -it --rm -v open-webui:/data alpine
```
Inside the container:
```sh
apk add apache2-utils sqlite
htpasswd -bnBC 10 "" your-new-password | tr -d ':'
sqlite3 /data/webui.db
```
```sql
UPDATE auth SET password='HASH' WHERE email='admin@example.com';
SELECT changes();
```
Exit with Ctrl+D. Emails are stored lower-case: a mixed-case address matches zero rows and sqlite3 prints nothing, so confirm with `SELECT changes();`.

## 2b. Docker one-liner (may fail: alpine/socat has no bash)
```bash
docker run --rm -v open-webui:/data alpine/socat EXEC:"bash -c 'apk add sqlite && echo UPDATE auth SET password='\''HASH'\'' WHERE email='\''admin@example.com'\''; | sqlite3 /data/webui.db'", STDIO
```

## 2c. Local install
From the `open-webui` directory:
```bash
sqlite3 backend/data/webui.db "UPDATE auth SET password='HASH' WHERE email='admin@example.com';"
```

## Full reset
To wipe everything (users, settings, chats, passwords) delete `webui.db`. Locate it from Python: `os.path.join(os.path.dirname(open_webui.__file__), "data", "webui.db")`, or `find / -name 'webui.db'`. Irreversible.

## Gotchas
- The volume name `open-webui` in the commands must match your container's data volume. The method edits `webui.db`.

## Checked
2026-11-07. Confirmed against the Open WebUI docs: troubleshooting/password-reset (read in full). Removed: the data-directory path line, the SQLite-only claim and the expected changes() value, none of which the page states.
Method: documentation only; no commands were run.
