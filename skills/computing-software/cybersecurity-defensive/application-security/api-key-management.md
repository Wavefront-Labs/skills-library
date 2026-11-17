---
id: computing-software.cybersecurity-defensive.application-security.api-key-management
name: api-key-management
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [api-key-management, api-keys, api-security, token-format, secret-scanning, rate-limiting]
level: practitioner
status: docs-checked
description: "Issue API keys to customers: prefix and checksum format, HTTPS only, 429 limits, revocation, GitHub secret scanning partner program."
sources: ["https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html", "https://github.blog/engineering/platform-security/behind-githubs-new-authentication-token-formats/", "https://docs.github.com/en/code-security/secret-scanning/secret-scanning-partnership-program/secret-scanning-partner-program"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API key management (provider side)

API keys limit abuse of public services and can gate access plans, but when issued to third-party clients they are
relatively easy to compromise. Design the format and handling for leaks.

## Key format (GitHub token design and partner guidance)
- **Identifiable prefix**: a company signifier plus token-type letter, for example GitHub's `ghp` (personal access
  token), `gho` (OAuth access), `ghu` (user-to-server), `ghs` (server-to-server), `ghr` (refresh). GitHub expects a
  prefix alone to cut secret scanning false positives to about 0.5%.
- **Separator `_`**: not a Base64 character, so a token cannot be mistaken for random strings such as SHA hashes, and a
  double-click selects the whole token.
- **Checksum**: GitHub puts a 32-bit checksum (CRC32, Base62-encoded, zero-padded) in the last 6 characters so fake
  tokens are rejected offline without a database lookup, while the random part keeps consistent entropy.
- **High entropy**: GitHub's new OAuth token format raised entropy from 160 to 178 bits at the same length.
- GitHub's partner guidance lists the same best practices: a uniquely defined prefix, high entropy random strings and a
  32-bit checksum.

## Using keys (OWASP REST Security)
- Provide HTTPS endpoints only, so API keys are protected in transit.
- Require an API key on every request to the protected endpoint.
- Return `429 Too Many Requests` when requests arrive too quickly; revoke the key if the client violates the usage
  agreement.
- Do not rely only on API keys to protect sensitive, critical or high-value resources.
- Never put keys in the URL (for example `?apiKey=...`): URLs are captured in web server logs.

## Leak detection: GitHub secret scanning partner program
- Join by emailing secret-scanning@github.com; supply a human-readable secret type name, a precise regular
  expression, a test account and the endpoint URL.
- When a match is found in a public source GitHub sends an HTTP `POST` with a JSON array of `token`, `type`, `url`
  and `source`. Handle large arrays without timing out.
- Verify the request: headers `Github-Public-Key-Identifier` and `Github-Public-Key-Signature`; fetch keys from
  `https://api.github.com/meta/public_keys/secret_scanning` and verify with `ECDSA-NIST-P256V1-SHA256` over the raw
  body (do not re-serialise the JSON).
- Treat every reported secret as public and compromised: revoke it and notify the affected user.
- Optional false-positive feedback may use the raw token or its SHA-256 hash, labelled `true_positive` or
  `false_positive`.

## Verify
Keys carry the prefix and checksum, are only accepted over HTTPS, are never in URLs, exceed-limit callers get 429, and
a test key committed to a public repository reaches your endpoint and is revoked.

## Checked
Method: docs-checked 2026-11-09 against the OWASP REST Security Cheat Sheet (API keys, HTTPS, credentials in URLs),
the GitHub blog "Behind GitHub's new authentication token formats" and the GitHub secret scanning partner program
page (read in full). Removed unconfirmed claims: 128-bit minimum entropy, hashing keys at rest, metadata fields,
scopes and IP allowlists, two active keys for rotation, expiry emails, header names for sending keys, and
GitLab programmes.
