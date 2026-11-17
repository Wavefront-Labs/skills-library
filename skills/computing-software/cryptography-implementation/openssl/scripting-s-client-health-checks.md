---
id: computing-software.cryptography-implementation.openssl.scripting-s-client-health-checks
name: scripting-s-client-health-checks
category: computing-software
field: cryptography-implementation
product: openssl
tags: [openssl, cryptography-implementation, s-client-scripting, openssl-s-client, certificate-expiry, monitoring, ci]
level: practitioner
status: verified
description: "Script openssl s_client checks for CI and cron: non-interactive input, timeouts, exit codes, extracting expiry and chain details, and alerting on near-expiry certs."
sources: ["https://docs.openssl.org/3.0/man1/openssl-s_client/", "https://docs.openssl.org/3.0/man1/openssl-x509/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scripting s_client health checks

## Non-interactive basics
- Always feed stdin: `</dev/null` or `echo Q |`, or s_client waits for input.
- Wrap with `timeout 10` since s_client has no connect timeout of its own.
- Exit status is 0 even when verification fails; check `Verify return code` or use `-verify_return_error`.

## Expiry check
```sh
#!/bin/sh
host=$1; port=${2:-443}; days=${3:-21}
cert=$(timeout 10 openssl s_client -connect "$host:$port" -servername "$host" \
        -verify_return_error </dev/null 2>/dev/null | openssl x509) || { echo "CRIT $host handshake/verify failed"; exit 2; }
if ! echo "$cert" | openssl x509 -noout -checkend $((days*86400)) >/dev/null; then
  echo "WARN $host expires $(echo "$cert" | openssl x509 -noout -enddate)"; exit 1
fi
echo "OK $host"
```
`-checkend N` returns 1 if the cert expires within N seconds.

## Other extractions
```sh
openssl s_client -connect h:443 -servername h -showcerts </dev/null 2>/dev/null | grep -c 'BEGIN CERT'  # chain length
openssl s_client -connect h:443 -servername h -brief </dev/null 2>&1 | grep -E 'Protocol|Ciphersuite'
```

## Pitfalls
- Forgetting `-servername`: SNI-based servers return a default cert and the check passes on the wrong one.
- Checking from inside the network only; also probe from outside.
- Parsing human-readable output that changes between OpenSSL versions; prefer `x509` options.

## Verify
- [ ] Job tested against an expired test host (badssl.com `expired.badssl.com`) and alerts correctly.

## Checked
- OpenSSL 3.2.3 against a local `s_server` with a private CA: the expiry script returned CRIT (CA untrusted), OK (trusted via `SSL_CERT_FILE`) and WARN (60-day threshold on a 30-day cert); `s_client` exited 0 with a failed verification and 1 with `-verify_return_error`; `-showcerts` count, `-brief` Protocol and Ciphersuite lines, and `-checkend` behaved as written.
- `expired.badssl.com` returns `Verify return code: 10 (certificate has expired)`. `s_client -help` lists no connect timeout option, so the `timeout` wrapper is needed.
