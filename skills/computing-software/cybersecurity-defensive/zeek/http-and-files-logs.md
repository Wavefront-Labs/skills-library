---
id: computing-software.cybersecurity-defensive.zeek.http-and-files-logs
name: http-and-files-logs
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, http-log, files-log, fuid-pivot, file-extraction]
level: practitioner
status: docs-checked
description: "Use Zeek http.log and files.log together: method, host, uri, user_agent, MIME types, fuid and uid pivots from conn.log, and why files.log does not imply extraction."
sources: ["https://docs.zeek.org/en/current/reference/logs/http.html", "https://docs.zeek.org/en/current/reference/logs/files.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# http and files logs

**http.log** (`HTTP::Info`) records each request and reply in one entry, so it shows who requested, who responded, and what. Useful fields: `trans_depth`, `method`, `host`, `uri`, `version`, `user_agent`, the status response, response MIME types, and file IDs. With HTTPS replacing clear text it is quieter in many environments, but it still matters where HTTPS is exposed as HTTP.

Example reading: 192.168.4.76 sent an HTTP 1.1 GET for `/` on host testmyids.com with a curl user agent; the responder replied 200 OK with MIME type `text/plain` and a file ID (`fuid`). The `uid` matches the one in `conn.log`.

**files.log** (`Files::Info`) records files Zeek observed. An entry does not mean content was written to disk: configure Zeek to extract by type (the page's example extracts `application/x-dosexec`).

Investigation chain: start in `conn.log` (here 179604 bytes sent by the responder over port 80), take its `uid`, find the `http.log` entry, then follow its `fuid` into `files.log`, where the same file appears with its MIME type and any extracted file name.

Pivot rule: `uid` links connection-oriented logs; `fuid` links file records.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
