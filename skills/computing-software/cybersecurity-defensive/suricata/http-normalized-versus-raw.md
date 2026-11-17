---
id: computing-software.cybersecurity-defensive.suricata.http-normalized-versus-raw
name: http-normalized-versus-raw
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [http-normalization, http-raw, http-host, http-header-raw]
level: advanced
status: docs-checked
description: "Choose normalized or raw HTTP buffers: http.host versus .raw, http.uri versus .raw, http.header versus .raw, duplicate header joining."
sources: ["https://docs.suricata.io/en/latest/rules/http-keywords.html", "https://docs.suricata.io/en/latest/rules/differences-from-snort.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Normalized versus raw HTTP

- `http.host` lowercases and drops the port; `nocase` is not allowed with it. `http.host.raw` keeps the original, including the port.
- `http.uri` normalizes the path (a doubled leading slash becomes one). `http.uri.raw` keeps it; it does not allow spaces, so text after a space lands in `http.protocol`.
- `http.header` strips trailing whitespace and tabs from values and excludes cookies. `http.header.raw` does not, and can match repeated headers normalization would merge.
- Repeated headers are joined with a comma and space.

`http.header_names` begins with a CRLF and ends with an extra CRLF, so a rule can match exact header order, presence or absence.

From the Snort comparison: Suricata does not add Snort's extra trailing CRLF to `http_header` (`http_raw_header` keeps CRLF CRLF), normalizes spacing after the colon, and removes Cookie and Set-Cookie lines from `http_header`. `+` to space needs `query-plusspace-decode: yes` in the libhtp section.

## Checked

2026-11-08: read in full against the OISF/suricata doc/userguide rst source (rules/http-keywords and rules/differences-from-snort) read in full; the claims, names, values and examples left in this skill match the page text. Corrected the CRLF CRLF comparison to the page wording.

Method: documentation only; no commands were run.
