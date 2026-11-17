---
id: computing-software.cryptography-implementation.protocol-implementation.certificate-discovery-and-inventory
name: certificate-discovery-and-inventory
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, certificate-inventory, certificate-discovery, ct-logs, expiry-monitoring, pki]
level: practitioner
status: docs-checked
description: "Discover and inventory certificates: crt.sh identity search, tlsx scans for expired or untrusted certificates, and cert-manager renewal timing."
sources: ["https://crt.sh/", "https://github.com/projectdiscovery/tlsx", "https://cert-manager.io/docs/usage/certificate/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Certificate discovery and inventory

## Sources
1. **CT-based search with crt.sh**: the search page accepts an identity (domain name, organisation name, etc.), a SHA-1 or SHA-256 certificate fingerprint, or a crt.sh ID. Search your domains to find certificates issued by teams you did not know about.
2. **Network scans with tlsx** (ProjectDiscovery TLS grabber): `-u host` or `-l file` for targets and `-p` for ports (default 443). Probes include `-san`, `-cn`, `-so`, `-tv` (TLS version), `-cipher`, `-hash` (md5, sha1, sha256 fingerprints), `-se` (serial), `-jarm` and `-ja3`. Misconfiguration filters: `-ex` expired, `-ss` self-signed, `-mm` mismatched, `-re` revoked, `-un` untrusted, `-wc` wildcard. `-j` gives JSON lines and `-cert` / `-tc` add the certificate or chain to JSON output. Scan internal ranges and non-443 ports too, via the `-p` option.
3. **cert-manager** (Kubernetes): each `Certificate` resource names the target `Secret` holding the key and signed certificate, and carries `duration` and `renewBefore`.

## Inventory fields
Subject and SANs, issuer, serial, notAfter, key type and size, location(s), owner team, renewal method, dependent services. (A suggested field list, not defined by the sources.)

## Operate
- cert-manager renews automatically: by default at 2/3 of the certificate's duration, or `renewBefore` before expiry if set (`spec.duration` must exceed `spec.renewBefore`; minimum duration 1 hour, minimum effective `renewBefore` 5 minutes). It sets `status.renewalTime`, so alert on certificates past that time that have not renewed.
- Setting `renewBefore` very close to `duration` can cause a renewal loop.

## Verify
- [ ] Every certificate found by CT search maps to an owner.
- [ ] Scan results are diffed regularly against the inventory.

## Checked
Method: docs-checked 2026-11-09 against the crt.sh search page, the tlsx README (flags list) and the cert-manager Certificate usage page (renewal behaviour).
Removed as unconfirmed: the crt.sh `output=json` query URL, nmap ssl-cert, cloud provider API commands, the kubectl TLS secret field selector, host file searches, private CA issuance log sources, 30/14/7-day alert thresholds, weak-key flagging rules and CBOM advice.
