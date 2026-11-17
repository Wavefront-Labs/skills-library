---
id: computing-software.systems-network-administration.pki-tls-administration.pebble-acme-test-server
name: pebble-acme-test-server
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [pebble-acme-test-server, pki-acme-testing, pebble, acme-test, challtestsrv, boulder, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Test ACME clients against Pebble before production: trust its test CA, validation ports, skipped validation and injected badNonce errors."
sources:
  - https://github.com/letsencrypt/pebble
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pebble and test ACME servers
Goal: exercise ACME client and renewal logic against a throwaway CA.
```
docker run -p 14000:14000 -p 15000:15000 -e "PEBBLE_VA_NOSLEEP=1" ghcr.io/letsencrypt/pebble
```
The ACME directory is then at `https://localhost:14000/dir` and the management interface at `https://localhost:15000`.
- Pebble is a miniature Boulder for testing only. It drops all state between runs and randomises its keys, certificates and `/directory` URLs, so clients cannot hardcode them.
- Trust: Pebble serves HTTPS only with a certificate from a test CA (`test/certs/pebble.minica.pem` in the repo). Give that file to your client's trusted-roots option. Do not add `pebble.minica.pem` to a system-wide trust store or production code; its private key is public in the repo. Pebble's own root and intermediate are regenerated on every launch (`GET https://localhost:15000/roots/0` and `/intermediates/0`).
- Validation ports: Pebble validates HTTP-01 on port 5002 and TLS-ALPN-01 on port 5001 by default (config `httpPort` and `tlsPort`).
- DNS-01: Pebble uses the system resolver unless started with `-dnsserver`. The `pebble-challtestsrv` mock server can serve DNS data (its management interface is on port 8055; the docker-compose file wires it up).
- Speed: by default Pebble sleeps a random 0 to 15 seconds between validation attempts; `PEBBLE_VA_NOSLEEP=1` removes that and `PEBBLE_VA_SLEEPTIME` sets the maximum.
- Skip validation: `PEBBLE_VA_ALWAYS_VALID=1` treats every challenge as successful.
- badNonce: by default Pebble rejects 5 percent of valid nonces as invalid to check clients retry; `PEBBLE_WFE_NONCEREJECT=90` raises it and `=0` disables it.
- Authorization reuse: Pebble reuses valid authorizations in new orders 50 percent of the time (`PEBBLE_AUTHZREUSE`), so clients must check order and authorization status.
- Limits: Pebble does not enforce rate limits, so it cannot test rate-limit handling, and it does less input validation than Boulder. It does not act as an OCSP responder.
- Boulder is the full Let's Encrypt server but multi-process and operationally complex (it needs MariaDB and gRPC among other dependencies).
Gotcha: never point production services at Pebble; it is built to make production use inconvenient.

Verify:
- [ ] The client completes an order while nonce rejection is enabled.
- [ ] The client works with `PEBBLE_VA_NOSLEEP` unset (it polls rather than assuming timing).

## Checked
Checked against the Pebble README (usage, ports, environment variables, trust warnings, limitations).
Removed: the step-ca and Let's Encrypt staging claims, the certbot and `REQUESTS_CA_BUNDLE` command, and the port 8055 as DNS claim (the README gives 8055 as the challtestsrv management interface).
Method: docs-only read of cited pages, 2026-11-08
