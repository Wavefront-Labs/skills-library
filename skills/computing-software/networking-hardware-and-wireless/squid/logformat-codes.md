---
id: computing-software.networking-hardware-and-wireless.squid.logformat-codes
name: logformat-codes
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, logformat, log-format, format-codes, squid-log]
level: advanced
status: draft
description: "Build custom log lines with logformat: encoding, alignment, width, common % codes and the predefined formats."
sources:
  - https://www.squid-cache.org/Doc/config/logformat/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# logformat
Syntax: `logformat <name> <format specification>`: literal text plus `%` codes. Each code takes an optional encoding prefix (`"` quoted, `[` Squid custom, `#` URL, `/` shell-like, `'` raw), `-` for left alignment, a `[width_min][.width_max]` width and an `{arg}`. `%%` is a literal percent.

Key codes: `%ts`/`%tu`/`%tl`/`%tg` times, `%tr` response time ms, `%>a` client IP, `%Ss` request status, `%Sh` hierarchy status, `%>Hs` HTTP status, `%<st` reply size, `%rm` method, `%ru` URL, `%un` user name, `%mt` MIME type, `%<a` server IP, `%>h` request header.

Predefined:
```
logformat squid      %ts.%03tu %6tr %>a %Ss/%03>Hs %<st %rm %ru %[un %Sh/%<a %mt
logformat common     %>a - %[un [%tl] "%rm %ru HTTP/%rv" %>Hs %<st %Ss:%Sh
```
Also `combined`, `referrer`, `useragent`. `log_mime_hdrs` on appends MIME headers to squid, common and combined.
