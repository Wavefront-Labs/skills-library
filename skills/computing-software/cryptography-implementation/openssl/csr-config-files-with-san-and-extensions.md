---
id: computing-software.cryptography-implementation.openssl.csr-config-files-with-san-and-extensions
name: csr-config-files-with-san-and-extensions
category: computing-software
field: cryptography-implementation
product: openssl
tags: [cryptography-implementation, openssl, csr, x509, openssl-req-config, subject-alt-name, openssl-req, certificate-signing-request]
level: practitioner
status: verified
description: "Write reusable openssl req config files: non-interactive DN, SAN lists, requested extensions, UTF-8 subjects and env-var substitution, then verify the CSR."
sources: ["https://docs.openssl.org/3.0/man1/openssl-req/", "https://docs.openssl.org/3.0/man5/config/", "https://docs.openssl.org/3.0/man5/x509v3_config/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSR config files with SAN and extensions

One-off `-subj`/`-addext` lines are fine at a prompt; anything repeated (renewals, automation,
many hosts) belongs in a config file so the CSR is reproducible and reviewable.

## A complete server CSR config
```
# server.cnf
[req]
prompt             = no
default_md         = sha256
distinguished_name = dn
req_extensions     = v3_req
string_mask        = utf8only
utf8               = yes

[dn]
C  = GB
O  = Example Ltd
CN = api.example.com

[v3_req]
subjectAltName   = @alt
keyUsage         = critical, digitalSignature
extendedKeyUsage = serverAuth

[alt]
DNS.1 = api.example.com
DNS.2 = api-eu.example.com
IP.1  = 10.20.0.15
```
```
openssl req -new -config server.cnf -key api.key -out api.csr
# or create key and CSR together (3.x: -noenc replaces -nodes)
openssl req -new -config server.cnf -newkey ec -pkeyopt ec_paramgen_curve:P-256 \
  -noenc -keyout api.key -out api.csr
```

## Parameterise with environment variables
```
[alt]
DNS.1 = $ENV::PRIMARY_HOST
```
`PRIMARY_HOST=web1.example.com openssl req -new -config server.cnf ...`. An unset variable is an
error, which is what you want. For a variable-length SAN list, generate the `[alt]` section
from a template rather than encoding commas into one variable.

## Rules that save renewals
- Hostnames go in SAN. CN is optional for public CAs and ignored by browsers; keep it equal to
  the first SAN for old tooling.
- `prompt = no` means the `[dn]` keys are values, not prompts; with `prompt = yes` the same
  section holds prompt text, a frequent source of CSRs whose CN reads "Common Name".
- The CA decides the final extensions. `req_extensions` only requests them; public CAs ignore most
  of what you put there except SANs. Private CAs must copy deliberately (see the extensions skill).
- Wildcards: `DNS.1 = *.example.com` covers one label only, not the apex; list both.
- IDNs: put the A-label (`xn--...`) in DNS SANs.
- `-subj` on the command line overrides `[dn]`; escape `/` inside values as `\/`.

## Check before you submit
```
openssl req -in api.csr -noout -verify -text \
  | grep -E "verify OK|Subject:|DNS:|IP Address|Public-Key|Signature Algorithm"
openssl req -in api.csr -noout -subject -nameopt RFC2253
```
`-verify` checks the CSR self-signature (proof of possession). Confirm the key size/curve and
that every SAN is present before anything else.

## Gotchas
- Tested on OpenSSL 3.2.3: the config above builds a CSR with `verify OK`; `$ENV::NAME` unset gives `variable has no value`.
- `default_md` matters on old builds that defaulted to SHA-1; set it explicitly.
- Some public CAs reject CSRs with `extendedKeyUsage` or `keyUsage` they don't support; drop
  them for public issuance if the order fails.
- Store the config in version control next to the service; the key never goes there.

## Verify
- [ ] `openssl req -verify` prints `verify OK`.
- [ ] SAN list in the CSR equals the hosts the service answers on.
- [ ] Renewal is one command using the same config.
