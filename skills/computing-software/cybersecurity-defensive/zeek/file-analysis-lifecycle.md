---
id: computing-software.cybersecurity-defensive.zeek.file-analysis-lifecycle
name: file-analysis-lifecycle
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, file-analysis, file-events, mime-sniffing, fa-file]
level: practitioner
status: docs-checked
description: "Zeek file analysis: supported protocols, file lifecycle events (file_new, file_sniff, file_state_remove), file UIDs linking to connections, and magic signatures for MIME types."
sources: ["https://docs.zeek.org/en/current/frameworks/file-analysis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# file analysis lifecycle

The file analysis framework (FAF) presents files uniformly regardless of the transporting protocol, analogous to connection analysis. Shipped file analysis covers FTP, HTTP, IRC, Kerberos, MIME, RDP, SMTP and SSL/TLS/DTLS. Further analyzers can come from packages.

Lifecycle events: `file_new`, `file_over_new_connection`, `file_sniff`, `file_timeout`, `file_gap` and `file_state_remove`. Each gives the connection and protocol carrying the file, bytes so far, and MIME type.

```
event file_state_remove(f: fa_file)
    {
    print f$id;
    for ( cid in f$conns )
        print f$conns[cid]$uid;
    print f$source;
    }
```

Files are identified by a string like a connection UID, and hold references to the connection or connections that carried them. Protocol analyzers may extend `fa_file`; for example the default HTTP scripts expose `f$http`. Check optional fields with `a?$b` before reading.

File type identification uses Zeek's own content signatures, delivered as MIME types in `file_sniff` (the `meta$mime_type` field may be absent, so test it). The signatures live in `scripts/base/frameworks/files/magic/`. Zeek does not use libmagic.

General file information (size, last data time, MIME type) is logged in `files.log` whichever analyzers act on the file.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
