---
id: computing-software.cybersecurity-defensive.suricata.http-sticky-buffers
name: http-sticky-buffers
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [http-keywords, http-uri, http-method, http-user-agent, urilen]
level: practitioner
status: docs-checked
description: "Inspect HTTP fields with sticky buffers: request, response and either-direction buffers, urilen, flow direction forcing and legacy names."
sources: ["https://docs.suricata.io/en/latest/rules/http-keywords.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HTTP sticky buffers

Follow a buffer with `content`, `pcre`, `startswith`, `bsize` and so on.

- Request: `http.uri`, `http.method`, `http.host`, `http.user_agent`, `http.referer`, `http.request_line`, `http.request_header`, `http.request_body`, `http.accept`, `http.accept_enc`, `http.accept_lang`, `urilen`, `file.name`.
- Response: `http.stat_code`, `http.stat_msg`, `http.response_line`, `http.response_header`, `http.response_body`, `http.server`, `http.location`.
- Either: `http.header`, `http.cookie`, `http.content_type`, `http.content_len`, `http.connection`, `http.protocol`, `http.start`, `http.header_names`, `file.data`.

Force a direction with `flow:to_server` or `flow:to_client` for buffers that work in both (`http.content_len`, `http.content_type`, `http.header_names`, `http.start`).

`urilen` compares the normalized URI length with `<`, `>` or a range such as `10<>12`. Use hex `|3a 20|` for a colon and space. `http.user_agent` usually outperforms `http.header`.

Legacy: `http_client_body`, `http_server_body` and `file_data` are replaced by `http.request_body`, `http.response_body` and `file.data`.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/http-keywords) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
