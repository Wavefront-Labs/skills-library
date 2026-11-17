---
id: computing-software.web-development.bun.serve-tls-sni
name: serve-tls-sni
category: computing-software
field: web-development
product: bun
tags: [serve-tls, mutual-tls, sni, client-certificates]
level: advanced
status: docs-checked
description: "Serve HTTPS from Bun.serve: tls key and cert, mutual TLS with requestCert and CRL, multiple certificates via serverName SNI, and common mistakes."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/runtime/http/tls.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
Bun.serve({
  tls: { key: Bun.file("./key.pem"), cert: Bun.file("./cert.pem") },
  fetch() { return new Response("secure"); },
});

// mutual TLS with revocation checking
Bun.serve({
  tls: {
    key: Bun.file("./key.pem"), cert: Bun.file("./cert.pem"),
    ca: Bun.file("./client-ca.pem"), requestCert: true,
    crl: Bun.file("./client-ca.crl.pem"),
  },
  fetch() { return new Response("mTLS"); },
});

// SNI: array of tls objects
Bun.serve({ tls: [{ key, cert, serverName: "a.example.com" }, { key: k2, cert: c2, serverName: "*.b.example.com" }], fetch() { return new Response("x"); } });
```

Gotchas:
- `key` and `cert` are PEM contents (string, `BunFile`, `Buffer`), not file paths; `passphrase` decrypts an encrypted key.
- `ca` replaces the default Mozilla list and alone does not request client certs; set `requestCert: true`. `rejectUnauthorized: false` accepts clients without a verifiable cert.
- `crl` only matters with `requestCert`.
- An array of key/cert pairs inside one `tls` object uses only the last pair; for several certificates use an array of `tls` objects with `serverName`.
- Wildcard `*` matches exactly one label; names are case-insensitive; duplicate `serverName` keeps the later entry.
- `NODE_TLS_REJECT_UNAUTHORIZED` does not change server behavior.

## Checked

2026-11-04. Confirmed against the Bun docs page runtime/http/tls: key and cert as contents not paths, passphrase, ca replacing the Mozilla list, requestCert needed for client certs, rejectUnauthorized false, NODE_TLS_REJECT_UNAUTHORIZED having no effect, crl with requestCert, last key/cert pair used in an array, array of tls objects with serverName, later duplicate replacing earlier, case-insensitive names and single-label wildcard. Nothing removed.
Method: documentation only; no commands were run.
