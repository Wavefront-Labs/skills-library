---
id: computing-software.cybersecurity-defensive.suricata.rule-option-syntax-and-buffers
name: rule-option-syntax-and-buffers
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [rule-options, sticky-buffers, content-modifiers, noalert]
level: practitioner
status: docs-checked
description: "Rule option syntax: escaping, noalert, old-style content modifiers versus sticky buffers, and normalized buffers."
sources: ["https://docs.suricata.io/en/latest/rules/intro.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Option syntax, sticky buffers and noalert

- Options: `keyword: settings;` or flag-only `keyword;`.
- Escape `;`, `"` and `\` inside values.
- `noalert` suppresses the alert while other actions still apply. It suits state tracking with flowbits, xbits or datasets, and in IPS mode can drop silently.

## Two styles

- Content modifier (older): `content:"index.php"; http_uri;` applies to the preceding content.
- Sticky buffer (newer): name the buffer first, then following keywords apply to it: `http_response_line; content:"403 Forbidden";`.

## Normalized buffers

HTTP and reassembly processing produce normalized copies with anomalies removed and packets combined. All HTTP keywords, reassembled streams, and TLS, SSL, SSH, FTP and DCE/RPC buffers are normalized, with exceptions such as `http_raw_uri`.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/intro) read in full; the claims, names, values and examples left in this skill match the page text. Nothing else was removed.

Method: documentation only; no commands were run.
