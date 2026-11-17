---
id: computing-software.cybersecurity-defensive.suricata.sticky-buffer-transforms
name: sticky-buffer-transforms
category: computing-software
field: cybersecurity-defensive
product: suricata
tags: [transforms, to-lowercase, from-base64, gunzip, dotprefix]
level: advanced
status: docs-checked
description: "Preprocess buffers with transforms such as to_lowercase, url_decode, from_base64, gunzip, xor, subslice, dotprefix, domain and tld."
sources: ["https://docs.suricata.io/en/latest/rules/transforms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Transforms

Placed after a sticky buffer and before match keywords; they run in order and chain. Not every buffer supports them yet.

`alert http any any -> any any (http.uri; to_lowercase; content:"admin"; sid:1;)`

- Case and space: `to_lowercase`, `to_uppercase`, `strip_whitespace`, `compress_whitespace`, `header_lowercase`, `strip_pseudo_headers`.
- Hashes: `to_md5`, `to_sha1`, `to_sha256` (raw digests).
- Decoding: `url_decode`, `from_base64: [bytes N][, offset N][, mode: strict|rfc4648|rfc2045]`, `xor` (`xor:"<hex_key>"`, `xor:extract <nbytes> <offset>`, `xor:offset <N>,"<hex_key>"`), `gunzip: max-size N`, `zlib_deflate: max-size N` (default cap 1024, 0 not allowed).
- Extraction: `pcrexform:"<regex>"` (first group), `subslice: offset[, nbytes][, truncate]`, `luaxform`.
- Domains: `dotprefix`, `domain`, `tld` (Public Suffix List).

Domain suffix example: `dns.query; dotprefix; content:".example.com"; endswith;`

## Checked

2026-11-04. Every transform, option and default above confirmed against the Suricata Transformations page.

Method: documentation only; no commands were run.
