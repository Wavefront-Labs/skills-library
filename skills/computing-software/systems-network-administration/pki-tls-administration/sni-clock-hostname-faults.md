---
id: computing-software.systems-network-administration.pki-tls-administration.sni-clock-hostname-faults
name: sni-clock-hostname-faults
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [sni-clock-hostname-faults, pki-troubleshooting, sni, clock-skew, hostname-mismatch, openssl-s-client, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Separate TLS failures caused by missing SNI, wrong system time, name mismatches, proxies and inconsistent backends, using openssl s_client."
sources:
  - https://docs.openssl.org/master/man1/openssl-s_client/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SNI, clock skew and hostname faults
Goal: the non-certificate causes of certificate errors. Diagnose with `openssl s_client`.
- SNI: `openssl s_client` fills the SNI extension from the name given to `-connect` if that is in DNS-name form; otherwise (or with no `-connect`) it sends "localhost". Connecting by IP therefore sends no useful SNI, and the server may return its default certificate. Set it explicitly with `-servername name` (the name is sent even if it is an IP address). `-noservername` suppresses the extension, which reproduces a client or library that sends no SNI.
- Compare certificates per backend: `openssl s_client -connect IP:443 -servername host` against each IP, and `-showcerts` to see the certificates the server sends (the list as sent, not a verified chain).
- Verification: `-verify_return_error` turns on server certificate verification and aborts the handshake on an error instead of continuing, so a failure shows up in the exit.
- Clock: a client or server with the wrong date sees "not yet valid" or "expired". Check the system date and time-sync status on both ends; VMs restored from snapshot and devices without a real-time clock are common culprits.
- Hostname: the name in the URL must match a subject alternative name; connecting to `localhost`, a short name or an IP needs a SAN that matches.
- Proxies: HTTPS interception replaces the certificate with one from a corporate CA; look at the issuer.
- Load balancers: backends holding different certificates produce intermittent errors; compare serial numbers per backend.
- Split-horizon DNS can send you to a different server than expected; resolve the name and test each address.
Gotcha: a "random" one-in-N failure is often one stale backend; repeat the `s_client` connection in a loop and compare serials.

Verify:
- [ ] Repeated connections return the same certificate serial.
- [ ] Client and server clocks agree.

## Checked
Checked against the openssl-s_client manual page (-connect, -servername, -noservername, -showcerts, -verify_return_error).
Removed: `timedatectl`, `chronyc`, `curl --resolve` and `dig` command specifics, the 5-minute notBefore backdating advice, the 1 second NTP threshold and the 20-attempt count (none are on the cited page). The clock, hostname, proxy and DNS points are general diagnostic guidance, not claims from the page.
Method: docs-only read of cited pages, 2026-11-08
