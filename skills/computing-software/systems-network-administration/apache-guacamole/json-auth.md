---
id: computing-software.systems-network-administration.apache-guacamole.json-auth
name: json-auth
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, json-auth, external-authentication, json-secret-key, hmac-sha256, aes-128-cbc, api-tokens, encrypted-json, embedding]
level: advanced
status: docs-checked
description: "Embed Guacamole in another app with encrypted, signed JSON auth: json-secret-key, payload fields, HMAC-SHA256 plus AES-128-CBC with zero IV, POST to /api/tokens, and debugging."
sources:
  - https://guacamole.apache.org/doc/gug/json-auth.html
  - https://guacamole.apache.org/doc/gug/external-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Encrypted JSON authentication

The external app builds a signed, encrypted block containing identity and connections.

Install: `guacamole-auth-json-1.6.0.jar` into `GUACAMOLE_HOME/extensions/`; restart Tomcat. Docker: `JSON_ENABLED=true`.

Config: `json-secret-key` (Docker `JSON_SECRET_KEY`): 32 hex digits (128 bits), e.g. generated via `echo -n "<PASSPHRASE>" | md5sum`. Expiry is per payload only.

Payload:
- `username` (`""` for anonymous), `expires` (UNIX epoch milliseconds; omitted means never)
- `connections`: object keyed by name with `protocol`, `parameters`, optional `id` (needed for sharing/shadowing)
- A joining entry uses `join` (target id) instead of `protocol`, with `read-only` as the main parameter.

Encoding steps:
1. Sign the plaintext with HMAC-SHA256 and prepend the binary signature.
2. Encrypt with AES-128-CBC, all-zero IV.
3. Base64-encode, then URL-encode (`+`, `=` matter).
4. Send as `data` in a POST to `/api/tokens`, or as a `data` query parameter on any page.

```
curl --data-urlencode "data=<BASE64_RESULT>" http://localhost:8080/guacamole/api/tokens
```
The source ships `doc/encrypt-json.sh HEX_KEY file.json` using OpenSSL as a reference.

Failure mode: bad signature, undecryptable data or expiry returns a generic invalid-credentials error; the Tomcat log gives the real cause. Use a future `expires` timestamp when testing.

Keep the secret key server-side only. Related: apache-guacamole.header-auth.

Verify: the curl returns an auth token JSON, and the connections appear for that session.

## Checked

2026-11-04. Confirmed against the Guacamole manual pages json-auth and external-auth: HMAC/SHA-256 signing with the signature prepended, 128-bit AES in CBC mode with an all-zero IV, 32-digit hex json-secret-key generated through md5sum of a passphrase, payload fields (username with empty string for anonymous, expires in epoch milliseconds, no expiry when omitted, connections with protocol, parameters and optional id, join and read-only), base64 plus URL-encoding, POST of data to /api/tokens or data query parameter, the invalid-credentials error with details only in the Tomcat logs, and doc/encrypt-json.sh as the OpenSSL reference script. Changed: log wording now matches the page (Tomcat logs).

Method: documentation only; no commands were run.
