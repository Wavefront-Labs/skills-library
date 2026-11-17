---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-tls-and-https-agent-options
name: nodejs-tls-and-https-agent-options
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, node-tls, node-crypto, nodejs, tls, https-agent, node-extra-ca-certs, reject-unauthorized, mtls, javascript]
level: practitioner
status: verified
description: "Configure Node.js TLS clients and servers: createSecureContext, https.Agent ca and servername, minVersion, ciphers, NODE_EXTRA_CA_CERTS, system CAs and never disabling checks."
sources: ["https://nodejs.org/api/tls.html", "https://nodejs.org/api/https.html", "https://nodejs.org/api/cli.html#node_extra_ca_certsfile"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js TLS and https Agent options

## Client with a private CA and client certificate
```js
import https from "node:https";
import fs from "node:fs";
const agent = new https.Agent({
  ca: [fs.readFileSync("corp-root.pem")],         // replaces default roots for this agent
  cert: fs.readFileSync("client.pem"),
  key: fs.readFileSync("client.key"),
  minVersion: "TLSv1.2",
  servername: "api.internal",                     // SNI and hostname check name when connecting by IP
  keepAlive: true,
});
https.get("https://api.internal/health", { agent }, res => res.resume());
```
To trust a private root **in addition to** public roots: `ca: [...tls.rootCertificates, corpRoot]`, or set
`NODE_EXTRA_CA_CERTS=/path/corp-root.pem` in the environment (read once at startup). Per the docs neither the well-known nor the extra certificates are used when `ca` is set explicitly, which is why the first example needs `ca` to name every root it needs.

## Server
```js
import tls from "node:tls";
const server = https.createServer({
  key, cert,                                      // cert = leaf + intermediates concatenated
  minVersion: "TLSv1.2",
  ciphers: "TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256",
  ecdhCurve: "X25519:P-256",
  requestCert: true, rejectUnauthorized: true, ca: [clientCa],   // mTLS
  SNICallback: (name, cb) => cb(null, contexts.get(name)),       // tls.createSecureContext per host
}, app);
```
In request handlers, `req.socket.getPeerCertificate()` and `req.socket.authorized` give the client identity.

## System trust
Node bundles Mozilla roots (`tls.rootCertificates` had 144 on Node 20). `--use-openssl-ca` uses the OpenSSL store; `--use-system-ca` (or `NODE_USE_SYSTEM_CA=1`) adds the OS store: added in v23.8.0 (Windows, macOS), non-Windows/macOS systems from v23.9.0, backported to v22.19.0/v24.6.0 for the env var.

## Never do this
- `NODE_TLS_REJECT_UNAUTHORIZED=0` or `rejectUnauthorized: false` in production; it disables all verification.
- Custom `checkServerIdentity` that returns `undefined` unconditionally.
Fix the trust configuration instead.

## Verify
- [ ] `openssl s_client` against the server shows the full chain and TLS 1.2+ only.
- [ ] Client fails against a server with a wrong-hostname certificate (checked: `ERR_TLS_CERT_ALTNAME_INVALID`; a private-CA server with IP and DNS SANs, mutual TLS and `servername` all behaved as described).
