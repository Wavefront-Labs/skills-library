---
id: computing-software.systems-network-administration.pki-tls-administration.acme-sh-dns-api
name: acme-sh-dns-api
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [acme-sh-dns-api, pki-acme-clients, acme-sh, dns-api, wildcard, zerossl, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Use acme.sh for DNS-01 and wildcard certificates with provider APIs, install the cert to a service and choose the CA."
sources:
  - https://github.com/acmesh-official/acme.sh/wiki
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# acme.sh with DNS APIs
Goal: shell-only ACME client for hosts without Python.
```
export CF_Token="..." CF_Account_ID="..."      # provider credentials, stored in account.conf
acme.sh --issue --dns dns_cf -d example.com -d '*.example.com'
acme.sh --install-cert -d example.com --key-file /etc/ssl/example.key --fullchain-file /etc/ssl/example.crt --reloadcmd "systemctl reload nginx"
acme.sh --set-default-ca --server letsencrypt
```
- The default CA is ZeroSSL; pass `--server` on each command or run `--set-default-ca --server letsencrypt`. Short names include `letsencrypt`, `letsencrypt_test` (staging), `zerossl` and `google`.
- Setup creates a daily cron job to check and renew; check `crontab -l`.
- DNS alias mode (`--challenge-alias aliasDomainForValidationOnly.com`) validates through a CNAME to another domain, so the main zone's credentials are not needed for it.
- `--keylength ec-256` selects ECDSA P-256 (the default key type in the README table).
- To test, issue with `--server letsencrypt_test`.
Gotcha: environment variables used when issuing (such as `CF_Token`) are saved in `~/.acme.sh/account.conf` and reused for renewals; use a scoped API token.
Verify:
- [ ] `crontab -l` shows the acme.sh renewal job.
- [ ] Installed cert expiry via `openssl x509 -noout -enddate`.

## Checked
2026-11-03. Confirmed in the acme.sh README and wiki (Server, dnsapi, DNS alias mode, How to issue a cert): `--issue --dns dns_cf`, `CF_Token` and `CF_Account_ID`, saving of variables in `~/.acme.sh/account.conf`, `--install-cert` with `--key-file`, `--fullchain-file` and `--reloadcmd`, default CA zerossl, `--set-default-ca --server`, short server names, `--challenge-alias`, `--keylength` and `ec-256`, daily cron job. `-enddate` is on the openssl-x509 page. Removed: `--dns dns_acmedns`, `--staging`, `acme.sh --list` (not on the pages) and the plain-text file mode wording.
Method: documentation only; no commands were run.
