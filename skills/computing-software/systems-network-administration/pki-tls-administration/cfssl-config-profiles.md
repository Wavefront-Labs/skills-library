---
id: computing-software.systems-network-administration.pki-tls-administration.cfssl-config-profiles
name: cfssl-config-profiles
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cfssl-config-profiles, pki-cfssl, cfssl, cloudflare, profiles, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Define cfssl signing profiles (server, client, intermediate) with usages, expiry and CRL/OCSP URLs in config.json."
sources:
  - https://github.com/cloudflare/cfssl
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/README.md
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/doc/cmd/cfssl.txt
  - https://raw.githubusercontent.com/cloudflare/cfssl/master/cli/gencert/gencert.go
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cfssl signing profiles
Goal: policy-controlled signing from JSON profiles.
`config.json` (the expiry values are examples):
```
{"signing":{"default":{"expiry":"2160h"},"profiles":{
 "intermediate":{"usages":["cert sign","crl sign"],"expiry":"43800h","ca_constraint":{"is_ca":true,"max_path_len":0,"max_path_len_zero":true}},
 "server":{"usages":["signing","key encipherment","server auth"],"expiry":"2160h"},
 "client":{"usages":["signing","client auth"],"expiry":"720h"}}}}
```
```
cfssl genkey -initca ca-csr.json | cfssljson -bare ca
cfssl gencert -ca ca.pem -ca-key ca-key.pem -config config.json -profile server app-csr.json | cfssljson -bare app
```
- `cfssl gencert -ca cert -ca-key key [-config config] [-profile profile] [-hostname hostname] CSRJSON` is the documented usage; `-hostname` overrides the SANs.
- A profile needs at least `expiry`. It is a Go duration, so the largest unit is the hour.
- If `default` is absent, cfssl uses usages `signing`, `key encipherment`, `server auth`, `client auth` with `8760h` (one year).
- The CSR JSON shown in the README has `hosts` (SANs), `key` (`algo`, `size`) and `names`; `CN` is the common name.
- Profile fields for revocation and AIA: `ocsp_url`, `crl_url`, and `issuer_urls` (AIA URLs of the issuer certificate).
- Other profile fields: `backdate`, `not_before`, `not_after`, `ocsp_no_check`, `name_whitelist` (regular expression for permitted SANs), `auth_key`, `remote`.
- `cfssljson -bare ca` writes `ca.pem`, `ca-key.pem` and `ca.csr`. The CA key is a plain PEM file, so protect it.
Keep the configuration in version control (without keys) and review changes like code, so profile or issuer drift is visible before it reaches production.
Gotcha: `max_path_len: 0` alone gives an intermediate with no path length constraint; add `"max_path_len_zero": true` to get pathlen 0 (cfssl.txt).
Gotcha: usages are spelled as cfssl names (`server auth`, `cert sign`), the list is in cfssl.txt; do not use OpenSSL spellings such as `serverAuth`.
Verify:
- [ ] `openssl x509 -noout -text -in app.pem` shows the expected usages and expiry.
- [ ] The intermediate certificate shows `pathlen:0` in its Basic Constraints.

## Checked
Confirmed 2026-11-08 against the cfssl README, doc/cmd/cfssl.txt (profile fields, usage names, defaults, path length note) and cli/gencert/gencert.go (gencert usage and flags). Removed: the claim that `cfssl certinfo` matches a profile (the pages do not describe it), the claim about unknown usage values failing late, and the statement that keys are written unencrypted (only "protect the key" kept). Fixed: the intermediate profile needed `max_path_len_zero`.
Method: docs-only read of cited pages, 2026-11-08
