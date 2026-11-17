---
id: computing-software.cybersecurity-defensive.zeek.signature-conditions
name: signature-conditions
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, signatures, signature-conditions, payload-regex, load-sigs]
level: practitioner
status: docs-checked
description: "Write Zeek signatures: header, content, dependency and context conditions, loading .sig files with -s, signature_files or @load-sigs, and the signature_match event."
sources: ["https://docs.zeek.org/en/current/frameworks/signatures.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# signature conditions

Zeek's Snort-style signature language is secondary to scripting. Format: `signature <id> { <attributes> }` with conditions and actions.

```
signature my-first-sig {
    ip-proto == tcp
    dst-port == 80
    payload /.*root/
    event "Found root!"
}
```

Load signature files with `-s`, by `redef signature_files += ...`, or `@load-sigs ./mysigs.sig` (relative to the script). The default extension is `.sig`, searched along ZEEKPATH. Load `base/frameworks/signatures/main.zeek` to turn matches into `Signatures::Sensitive_Signature` notices.

**Header** (first packet only): `src-ip`/`dst-ip` (IPv6 in square brackets), `src-port`/`dst-port`, `ip-proto tcp|udp|icmp|icmp6|ip|ip6`, with comparison operators and comma lists such as `5,7-10`. General form: `header ip[16:4] == 1.2.3.4/16` with size 1, 2 or 4 bytes and optional `& mask`.

**Content**: `payload /regex/` matches raw payload (the reassembled stream for TCP; each packet otherwise). Analyzer-specific forms: `http-request`, `http-request-header`, `http-request-body`, `http-reply-header`, `http-reply-body`, `ftp`, `finger`. Their analyzer must be active, which needs its script loaded.

**Dependency**: `requires-signature [!] id`, `requires-reverse-signature [!] id`.

**Context** (evaluated last): `eval <function>`, `payload-size`, `same-ip`, `tcp-state`, `udp-state`.

Each signature reports at most once per connection. `payload` cannot match headers. With HTTP pipelining, multiple conditions may be satisfied by different transactions.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
