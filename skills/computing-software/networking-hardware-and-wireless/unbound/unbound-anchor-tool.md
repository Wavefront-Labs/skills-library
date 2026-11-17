---
id: computing-software.networking-hardware-and-wireless.unbound.unbound-anchor-tool
name: unbound-anchor-tool
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-anchor, root-anchor, rfc7958, icannbundle, exit-code]
level: practitioner
status: docs-checked
description: "Use unbound-anchor to update the root trust anchor: options, the RFC 5011 then HTTPS fallback order, and why exit code 0 does not prove success."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound-anchor.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unbound-anchor tool
Behaviour: it tests whether the existing anchor file works. If not, and an update is possible, it uses the root update certificate: it fetches `root-anchors.xml` and its `.p7s` signature over HTTPS, checks them per RFC 7958 and verifies the signature. The file is updated only if all checks pass. It also performs RFC 5011 tracking when the DNSSEC information in DNS allows it; by default it tries the DNS route first (the manual says it is faster and lighter) and falls back to the XML download (`-F` forces the download). It does not update if the certificate is expired or the network is down. By default it prints almost nothing, even on errors, so the existing anchor stays usable.

Key options:
- `-a <file>` anchor file, read and written; the default location is set at build or install time (a builtin root key is written if the file is missing or empty).
- `-c <file>` root update certificate; the default is also an install-time path, and a builtin certificate is used if the file is missing or empty. The manual suggests refreshing it from the IANA `icannbundle.pem` file.
- `-u <name>` server, default `data.iana.org`; `-P <port>` default 443.
- `-f <resolv.conf>` use those resolvers; `-R` allows fallback to direct root queries.
- `-r <root.hints>` bootstrap hints; `-4` / `-6` restrict IP version.
- `-v` verbose (repeat for debug); `-l` prints builtin key and certificate.

Exit codes: 1 means the anchor was updated using the certificate (or the builtin was used); 0 means no update needed, an RFC 5011 update succeeded, or an error occurred. A 0 does not confirm the anchor is valid or current.

For Unbound to track the anchor itself, its user needs write access to the file and directory.

## Checked

2026-11-08. Read the unbound-anchor manual page source in full. Corrected the default file locations (install-time, not fixed paths, and no default icannbundle.pem file name) and the update order description.

Method: documentation only; no commands were run.
