---
id: computing-software.networking-hardware-and-wireless.haproxy.ocsp-stapling-and-auto-update
name: ocsp-stapling-and-auto-update
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, ocsp-stapling, ocsp-update, show-ssl-ocsp-response, ssl-ocsp]
level: practitioner
status: docs-checked
description: "Enable OCSP stapling in HAProxy via .ocsp files, ocsp-update on in a crt-list or crt-store, and inspect it with show ssl ocsp-response and ocsp-updates."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://docs.haproxy.org/3.0/management.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ocsp stapling and auto update
Stapling attaches an OCSP response to the TLS handshake (the TLS Certificate Status Request extension).

File method: for each PEM file HAProxy looks for a file at the same path with `.ocsp` appended; if one exists, stapling is enabled automatically. The content is optional; if not empty it must be a DER OCSP response that indicates a good status, is a single response for that PEM's certificate and is valid at load time. Otherwise it is ignored with a warning. The response needs the issuer's certificate to identify the certificate: if not in the PEM, it is loaded from a file with `.issuer` appended, or loading fails with an error. `issuers-chain-path` completed chains are not used by OCSP, so supply an additional `.issuer` file.

Update a response at runtime (stats socket):
```
openssl ocsp -issuer issuer.pem -cert server.pem -host ocsp.issuer.com:80 -respout resp.der
echo "set ssl ocsp-response $(base64 -w 10000 resp.der)" | socat stdio /var/run/haproxy.stat
```
`set ssl ocsp-response` takes the base64 DER response and applies the same checks as initial loading; it is not supported with BoringSSL.

Auto update:
```
frontend fe
    bind :443 ssl crt-list haproxy.list
# haproxy.list
server_cert.pem [ocsp-update on] foo.bar
```
- `ocsp-update [on|off]` (default off) works on a crt-list line, in a `crt-store` `load` (`load crt foobar.pem ocsp-update on`), or globally through `ocsp-update.mode`. The same certificate with conflicting values across crt-lists, or against an incompatible inherited global setting, raises an error.
- When on, HAProxy fetches a response whenever the certificate has an OCSP URI; the issuer must be known to build the certid. Each response is refreshed at least hourly and sooner if it expires earlier, with a minimum interval of 5 minutes. A certificate with an OCSP URI but no response gets one fetched right after init. Defaults can be changed with the global `ocsp-update.mindelay` (300 s) and `ocsp-update.maxdelay` (3600 s; must be higher than the min).
- Related globals: `ocsp-update.disable on` ignores all auto-update configuration; `ocsp-update.httpproxy <address>[:port]` sends updates through an HTTP proxy (HTTP only).
- Each update writes a log line headed `<OCSP-UPDATE>` with the certificate path, a numeric and text status, and failure and success counts. A pure HTTP error also emits a regular HTTP log line.
- Troubleshooting from the manual: with Let's Encrypt certificates, an IPv6 address from DNS and no outgoing IPv6 route fails; fix the route or set `httpclient.resolvers.prefer ipv4` in `global`. For an "OCSP response check failure", check that the provided issuer certificate is valid.
- Inspect: `show ssl ocsp-response [[text|base64] <id|path>]` lists response IDs (or dumps one; `text` is the default); `show ssl ocsp-updates` shows one line per response with next update, last successful update, counters and last status; `update ssl ocsp-response <certfile>` forces an update, only for certificates that already had a stored response; `show ssl cert <file>.ocsp` also shows the response.

## Checked
2026-11-08. Confirmed against the HAProxy 3.0 configuration manual (SSL PEM `.ocsp`/`.issuer` rules, crt-list and crt-store `ocsp-update` text and logging, `ocsp-update.*` globals, `issuers-chain-path` note) and management guide (`set ssl ocsp-response`, `show ssl ocsp-response`, `show ssl ocsp-updates`, `update ssl ocsp-response`, `show ssl cert`). Removed: version claims, the `ssl-default-bind-options` suggestion, the cron job, the Let's Encrypt OCSP end-of-service remark, the claim that stale responses disable stapling, and the `openssl s_client` verification. Read as sections of both documents only.
Method: documentation only; no commands were run.
