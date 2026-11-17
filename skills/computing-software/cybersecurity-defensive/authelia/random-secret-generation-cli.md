---
id: computing-software.cybersecurity-defensive.authelia.random-secret-generation-cli
name: random-secret-generation-cli
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, crypto-rand, secrets, random-string, hmac-secret, jwt-secret, secret-generation]
level: intro
status: docs-checked
description: "Generate strong Authelia secrets and client identifiers with authelia crypto rand, choosing length, charset and writing straight to files."
sources:
  - https://www.authelia.com/reference/cli/authelia/authelia_crypto_rand/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`authelia crypto rand` generates cryptographically secure random strings for use as encryption keys, HMAC keys and similar values.

```bash
authelia crypto rand --length 80
authelia crypto rand --charset alphanumeric
authelia crypto rand --charset rfc3986
authelia crypto rand --characters 0123456789ABCDEF
authelia crypto rand /path/to/secrets/SESSION_SECRET /path/to/secrets/JWT_SECRET
authelia crypto rand --file /path/to/secrets/STORAGE_ENCRYPTION_KEY
```

Options:

- `-n, --length` sets the length; the default is 72.
- `-x, --charset` is one of `ascii`, `alphanumeric` (default), `alphabetic`, `numeric`, `numeric-hex` and `rfc3986`.
- `--characters` sets an explicit alphabet.
- Positional arguments or `--file` (a list of files) write one unique random value per file instead of printing it.
- `--mode-files` (default `0600`) and `--mode-dirs` (default `0700`) set permissions on what it creates.

The session configuration page recommends a random alphanumeric string of 64 or more characters for `session.secret`; the default `--length` of 72 and `alphanumeric` charset satisfy that. Writing directly to files with the default `0600` mode avoids printing secrets to the terminal.

Check: `ls -l` on the created files shows mode `600`, and each file has a different value.

## Checked

2026-11-08. Read the full authelia crypto rand CLI page and the Session page. Confirmed flags (--length default 72, --charset default alphanumeric and values, --characters, --file, --mode-files 0600, --mode-dirs 0700) and positional file arguments. Removed the list of specific secrets, the RFC 3986 client ID claim and the _FILE remark, which the CLI page does not state.

Method: documentation only; no commands were run.
